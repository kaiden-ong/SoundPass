import speech_recognition as sr
import json
from playsound import playsound
import pyttsx3

def record_text(r):
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

def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return

def main(status, pw, engine):
    r = sr.Recognizer()
    while(1):
        text = record_text(r)
        if text == "stop":
            return None
        if status == "unlocked":
            if text == "lock door":
                output_text(text)
                return False
            else:
                output_text(text)
                engine.say('Your door is already unlocked')
                engine.runAndWait()
                # playsound('./audio/alr_unlocked.mp3')
                print("door is already unlocked")
                return None
        else:
            if text == "lock door":
                output_text(text)
                engine.say('Your door is already locked')
                engine.runAndWait()
                # playsound('./audio/alr_locked.mp3')
                print("the door is already locked")
                return None
            output_text(text)
            if text == "hey sound pass":
                password = record_text(r)
                output_text("password attempt: " + password)
                return password == pw

if __name__=="__main__":
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    with open('door.json', 'r') as file:
        data = json.load(file)
        door_status = {"status": data["door_status"]}
        password = data["password"]
    with open("output.txt", "w") as f:
        pass
    mainReturn = main(door_status["status"], password, engine)
    if mainReturn != None:
        if mainReturn:
            door_status["status"] = "unlocked"
            engine.say('Unlocking your door')
            engine.runAndWait()
            # playsound('./audio/unlocking.mp3')
            print("door unlocks")
        else:
            door_status["status"] = "locked"
            engine.say('Locking your door')
            engine.runAndWait()
            # playsound('./audio/locking.mp3')
            print("door locks")
    data["door_status"] = door_status["status"]
    with open('door.json', 'w') as file:
        json.dump(data, file)
    engine.stop()