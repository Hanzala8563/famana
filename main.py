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
from datetime import date as dt
from datetime import datetime as DT
import pywhatkit as kt
import webbrowser
import calendar
import os
import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
#assistant base


from randomRecommender import random_movie_recommendation
from cRecommender import referenced_recommendation

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
intents_json_DIR=".../intents.json"
intents_file=open(intents_json_DIR)
intents_json=json.load(intents_file)
intents_file.close()
##

##Recommender Systems
from randomRecommender import random_movie_recommendation
from cRecommender import referenced_recommendation
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
    
    h,m,s=time.split(':')
    var_A.set("It is {m} past to {h}".format(m=m,h=h))
    ROOT.update_idletasks()
    speaker.say("It is {m} past to {h}".format(m=m,h=h))
    speaker.runAndWait()

def tell_date():
    ty=dt.today().strftime('%Y-%m-%d')
    y,m,d=ty.split("-")

    today = dt.today()
    day_of_week=calendar.day_name[today.weekday()]

    var_A.set("Today is {d},{day}".format(day=day_of_week,d=d))
    ROOT.update_idletasks()
    speaker.say("Today is {d},{day}".format(day=day_of_week,d=int(d)))
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

def create_note():
    global recognizer
    speaker.say("What do you want to write onto your note?")
    var_A.set("What do you want to write onto your note?")
    ROOT.update_idletasks
    speaker.runAndWait()
    done=False
    NOTE_ROOT=".../notes"

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=1)
                user_command=recognizer.listen(mic)

                content_note=recognizer.recognize_google(user_command)
                content_note=content_note.lower()

                var.set(content_note)
                var_A.set("Choose a filename!")
                ROOT.update_idletasks

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic,duration=5)
                user_command=recognizer.listen(mic)

                filename=recognizer.recognize_google(user_command)
                var.set(filename)
                ROOT.update_idletasks
                filename=filename.lower()
                filename=NOTE_ROOT+"/"+filename+".txt"

                with open(filename,'w+') as f:
                    f.write(content_note+"\n")
                    done=True
                    speaker.say("I successfully created the note")
                    var_A.set("I successfully created the note")
                    ROOT.update_idletasks

        except speech_recognition.UnknownValueError:
            recognizer=speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            var_A.set("I did not understand you! Please try again!")
            ROOT.update_idletasks
            speaker.runAndWait()


def movie_recommendation():
    var_A.set("Nice activity! \n Is there a movie genre \n you particularly want?")
    ROOT.update_idletasks

    speaker.say("Nice activity!")
    speaker.say("Is there a movie genre you particularly want?")
    speaker.runAndWait()

    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=1)
        user_command=recognizer.listen(mic)

        recognized_user_command=recognizer.recognize_google(user_command)
        lowered_user_command=recognized_user_command.lower()

        var.set(lowered_user_command)
        ROOT.update_idletasks

    assistant.request(lowered_user_command)


    
def random_m():
    var_A.set("I got a new movie for you!")
    ROOT.update_idletasks
    
    speaker.say("I got a new movie for you!")

    rnd_movie=random_movie_recommendation()
    
    var_A.set(rnd_movie+"\n Enjoy watching!")
    speaker.say(rnd_movie)
    ROOT.update_idletasks
    

    speaker.say("Enjoy watching!")
    speaker.runAndWait()


def referenced_m():
    speaker.say("Please give me a movie example")
    speaker.runAndWait()   

    var_A.set("Please give me a movie example")
    ROOT.update_idletasks

    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=1)
        user_command=recognizer.listen(mic)
        recognized_user_command=recognizer.recognize_google(user_command)
        lowered_user_command=recognized_user_command.lower()

        uppered_user_command=string.capwords(lowered_user_command,sep=None)

        var.set(uppered_user_command)
        ROOT.update_idletasks

        rfrd_movies=referenced_recommendation(uppered_user_command)


        speaker.say("I've got 3 movie ideas for you!")
        speaker.say(rfrd_movies)

        var_A.set(rfrd_movies)
        ROOT.update_idletasks

        speaker.runAndWait()


def quit():
    assistant_responses=intents_json['intents'][13]['responses']
    random.shuffle(assistant_responses)
    speaker.say(assistant_responses[0])
    var_A.set(assistant_responses[0])
    ROOT.update_idletasks()
    ROOT.destroy()
    sys.exit(0)


mappings={
    "hello": hello,
    "tell_time" :tell_time,
    "open_google": open_google,
    "open_youtube":open_youtube,
    "search_data": search_data,
    "tell_date" :tell_date,
    "create_note": create_note,
    "movie_recommendation": movie_recommendation,
    "random_m":random_m,
    "referenced_m":referenced_m,
    "exit": quit
}


assistant =GenericAssistant('.../intents.json',intent_methods=mappings)
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



