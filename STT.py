import speech_recognition as sr
import json

def record_text(r):
    while(1):
        try:
            with sr.Microphone(device_index=3) as source2:
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

def main(door_status, pw):
    r = sr.Recognizer()
    while(1):
        text = record_text(r)
        if door_status["status"] == "unlocked":
            if text == "lock door":
                door_status["status"] = "locked"
                return False
            else:
                print("door is already unlocked")
                return True;
        else:
            output_text(text)
            if text == "stop":
                break
            if text == "hey sound pass":
                password = record_text(r)
                output_text("password attempt: " + password)
                return password == pw

if __name__=="__main__":
    with open('door.json', 'r') as file:
        data = json.load(file)
        door_status = {"status": data["door_status"]}
        password = data["password"]
    with open("output.txt", "w") as f:
        pass
    if main(door_status, password):
        door_status["status"] = "unlocked"
        print("door unlocks")
    else:
        print("door locks")
    data["door_status"] = door_status["status"]
    with open('door.json', 'w') as file:
        json.dump(data, file)