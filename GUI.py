#GUI
from tkinter import *
#GUI

#Data
import json
import random
#Data

#assistant base
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import datetime
import pywhatkit as kt
import webbrowser
#assistant base



##GUI
ROOT = Tk()
ROOT.title("VoiceAssistant")
ROOT.configure(bg='black')
ROOT.geometry("700x700")

var = StringVar()
var.set(" ")

var_A=StringVar()
var_A.set(" ")

LABEL = Label(ROOT, textvariable =var,bg='black',fg='cyan',font=("times new roman",20),padx=5,pady=200)
LABEL.pack()

LABEL_A=Label(ROOT,textvariable =var_A,bg='black',fg='red',font=("times new roman",20),padx=5,pady=400)
LABEL_A.pack()
##


##Data
intents_json_DIR="C:/Users/yasemin/Desktop/AI_Asistant/intents.json"
intents_file=open(intents_json_DIR)
intents_json=json.load(intents_file)
intents_file.close()
##


##VOICE ASSISTANT
recognizer=speech_recognition.Recognizer()
speaker=tts.init()
speaker.setProperty('rate',150,)

#Assistant functions
def hello():
    assistant_responses=intents_json['intents'][0]['responses']
    random.shuffle(assistant_responses)
    speaker.say(assistant_responses[0])
    var_A.set(assistant_responses[0])
    ROOT.update_idletasks()

    speaker.runAndWait()

def tell_time():
    time=datetime.datetime.now().strftime("%H:%M:%S")
    var_A.set(time)
    ROOT.update_idletasks()
    speaker.say("The time is {t}".format(t=time))
    speaker.runAndWait()

def open_google():
    webbrowser.open_new_tab("https://www.google.com")
    speaker.say("Google is open now")
    var_A.set("Google is open now")
    ROOT.update_idletasks()
    speaker.runAndWait()

def open_youtube():
    webbrowser.open_new_tab("https://www.youtube.com")
    speaker.say("Youtube is open now")
    var_A.set("Youtube is open now")
    ROOT.update_idletasks()
    speaker.runAndWait()

def search_data():
    global recognizer
    speaker.say("What do you want search on the internet?")
    var_A.set("What do you want search on the internet?")
    ROOT.update_idletasks()
    speaker.runAndWait()
    
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=1)
        user_command=recognizer.listen(mic)

        recognized_user_command=recognizer.recognize_google(user_command)
        lowered_user_command=recognized_user_command.lower()
       
      
        speaker.say("Searching...")
        var_A.set("Searching...")
        ROOT.update_idletasks()
        speaker.runAndWait()
        kt.search(str(lowered_user_command))


def quit():
    speaker.say("Bye")
    var_A.set("Bye")
    ROOT.update_idletasks()
    speaker.runAndWait()
    sys.exit(0)


mappings={
    "hello": hello,
    "tell_time" :tell_time,
    "open_google": open_google,
    "open_youtube":open_youtube,
    "search_data": search_data,
    "exit": quit
}


assistant =GenericAssistant('intents.json',intent_methods=mappings)
assistant.train_model()


while True:
    try:
        ROOT.update()
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=1)
            user_command=recognizer.listen(mic)
            
            recognized_user_command=recognizer.recognize_google(user_command)
            lowered_user_command=recognized_user_command.lower()
            
            first=lowered_user_command[0]
            full=first.upper()+lowered_user_command[1:]
            var.set(full)
            ROOT.update_idletasks()
            
            

        assistant.request(lowered_user_command)
        

    except speech_recognition.UnknownValueError:
        recognizer=speech_recognition.Recognizer()



