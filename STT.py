import speech_recognition as sr
import json
from playsound import playsound
import pyttsx3
from datetime import datetime, timedelta

def record_text(r, engine):
    while(1):
        try:
            with sr.Microphone(device_index=1) as source2:
                print("Adjusting for ambient noise... Please wait.")
                r.adjust_for_ambient_noise(source2, duration=.1)
                print("Microphone is now ready. Start speaking...")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")
            engine.say("Sorry I didn't catch that")
            engine.runAndWait()

def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return

def withinFive(first_time):
    if len(first_time) == 0:
        return False, 0
    
    current = datetime.now()
    time_locked = datetime.strptime(first_time, "%m/%d/%Y %H:%M:%S")
    delta = timedelta(minutes=5)

    if time_locked + delta < current:
        return False, 0
    
    minutes_left = (time_locked + delta - current).total_seconds() / 60
    return True, abs(int(minutes_left))

def main(status, pw, time_locked, engine):
    incorrect_counter = 3
    r = sr.Recognizer()
    ready, min_left = withinFive(time_locked)

    if ready:
        engine.say('Keypad locked for %s minutes' % min_left)
        engine.runAndWait()
        return None, None
    
    while(1):
        text = record_text(r, engine)
        if text == "stop":
            return None, None
        if status == "unlocked":
            if text == "lock door":
                output_text(text)
                return False, None
            else:
                output_text(text)
                engine.say('Your door is already unlocked')
                engine.runAndWait()
                # playsound('./audio/alr_unlocked.mp3')
                print("door is already unlocked")
                return None, None
        else:
            if text == "lock door":
                output_text(text)
                engine.say('Your door is already locked')
                engine.runAndWait()
                # playsound('./audio/alr_locked.mp3')
                print("the door is already locked")
                return None, None
            output_text(text)

            if text == "sound":
                engine.say('Hey there!')
                engine.runAndWait()
                while (incorrect_counter > 0):
                    password = record_text(r)
                    output_text("password attempt: " + password)
                    if password == pw:
                        return True, None
                    else:
                        incorrect_counter -= 1
                        if incorrect_counter == 0: break
                        string = "%s guesses remaining" % incorrect_counter
                        engine.say("Incorrect password, try again. %s" % string)
                        engine.runAndWait()
                engine.say("Too many incorrect guesses, locked for 5 minutes")
                engine.runAndWait()
                return None, datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            
        engine.say("Sorry I didn't catch that")
        engine.runAndWait()

if __name__=="__main__":
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)

    with open('door.json', 'r') as file:
        data = json.load(file)
        door_status = data["door_status"]
        password = data["password"]
        time_locked = data["time_locked"]

    with open("output.txt", "w") as f:
        pass

    unlocks, date_time = main(door_status, password, time_locked, engine)

    if unlocks != None:
        if unlocks:
            door_status = "unlocked"
            engine.say('Unlocking your door')
            engine.runAndWait()
            # playsound('./audio/unlocking.mp3')
            print("door unlocks")
        else:
            door_status = "locked"
            engine.say('Locking your door')
            engine.runAndWait()
            # playsound('./audio/locking.mp3')
            print("door locks")
        data["door_status"] = door_status
        with open('door.json', 'w') as file:
            json.dump(data, file, indent=4)

    if date_time != None:
        data["time_locked"] = date_time
        with open('door.json', 'w') as file:
            json.dump(data, file, indent=4)

    engine.stop()