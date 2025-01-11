import datetime
import os
import json
import pickle
import sys
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
#import random
import pyautogui
import psutil
import subprocess
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from elevenlabs import play
from elevenlabs.client import ElevenLabs
#from elevenlabs import set_api_key
#from api_key import api_key_data
#set_api_key(api_key_data)
client = ElevenLabs(
  api_key="your-api", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

#def engine_talk(query):
 #   audio = client.generate(
 #       text=query, 
 #       voice='Grace',
 #       model="eleven_monolingual_v1"
  #  )
 #   play(audio)

with open("D:\jarvis\jarvis\intents.json", 'r') as file:
    data = json.load(file)

model = load_model("D:\jarvis\jarvis\chat_model.h5")
with open("D:\\jarvis\\jarvis\\tokenizer.pkl", "rb") as f:
    tokenizer= pickle.load(f)

with open("D:\jarvis\jarvis\label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume=engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine= initialize_engine()
    engine.say(text)
    engine.runAndWait()

#speak("hello i miss you")

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        #print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r",end="", flush=True)
        print("Recognizing......" ,end="",flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r",end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ("AM" in t):
        speak(f"Good morning Nisha, it's {day} and the time is {t}")
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Nisha, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Nisha, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord")
        webbrowser.open("https://discord.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Dear today's schedule is ")
    week = {
        "monday": "Dear, from 9:00 am you have algorithm class, from 10:00 am you have DSA class, from 4:00 you have badminton match, from 7:30 pm you have practices class",
        "tuesday": "Dear, from 9:00 am you have DSA class, from 11:00 am you have AI class, from 2:00 pm you have python class",
        "wednesday": "Dear, from 9:00 am you have algorithm class, from 10:00 am you have DSA class, from 7:30 pm you have practices class",
        "thursday": "Dear, today is full day classes",
        "friday": "Dear, today is full day classes",
        "saturday": "Dear, today is a relaxed day, from 9:00 am going for outing",
        "sunday": "Dear, today is holiday, but keep an eye on upcoming deadlines and solve practice questions"
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile("C:\Windows\System32\calc.exe")
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile("C:\\Windows\\System32\\notepad.exe")
    elif "paint" in command:
        speak("opening paint")
        subprocess.run(["start", "mspaint"], shell=True)
   
def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im CalculatorApp.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif "paint" in command:
        speak("closing paint")
        os.system("taskkill /f /im mspaint.exe")

def browsing(query):
    if 'google' in query:
        speak("Dear, what should i search on google..")
        s = command().lower()
        # Open Google Chrome with the search query
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open(f"https://www.google.com/search?q={s}")
        time.sleep(5)  # Waits for 10 seconds
        speak("close google.")
        time.sleep(10)  # Waits for 10 seconds
        
        # Close Google Chrome
        os.system("taskkill /f /im chrome.exe")
        speak("I have closed Google Chrome.")
    #elif 'edge' in query:
     #   speak("opening your microsoft edge")
     #   os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Dear our system have {percentage} percentage battery")
    
    if percentage>=80:
        speak("Dear we could have enough charging to continue our work")
    elif percentage>=40 and percentage<=75:
        speak("Dear we should connect our system to charging point to charge our battery")
    else:
        speak("Dear we have very low power, please connect to charging otherwise system should be off...")




def classify_and_respond(query, tokenizer, model, label_encoder):
    # Preprocess the query
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query.lower()]), maxlen=20, truncating='post')
    result = model.predict(padded_sequences)
    tag = label_encoder.inverse_transform([np.argmax(result)])[0]
    predicted_index = np.argmax(result)
    predicted_tag = label_encoder.inverse_transform([predicted_index])[0]

        # Handle datetime tag dynamically
    # Handle datetime tag dynamically
    if predicted_tag == "datetime":
        now = datetime.datetime.now()
        
        # Parse query to determine if the user asked for day, date, or time
        if "day" in query:
            return f"Today is {now.strftime('%A')}."  # Example: "Today is Thursday."
        elif "date" in query:
            return f"Today's date is {now.strftime('%d %B %Y')}."  # Example: "Today's date is 09 January 2025."
        elif "time" in query:
            return f"The current time is {now.strftime('%I:%M %p')}."  # Example: "The current time is 02:45 PM."
        else:
            # Default response if it's a general query about datetime
            today_date = now.strftime("%A, %d %B %Y")
            current_time = now.strftime("%I:%M %p")
            return f"Today is {today_date}, and the current time is {current_time}."

    # Find matching intent
    for intent in data['intents']:
        if intent['tag'] == tag:
            response = np.random.choice(intent['responses'])
            return response

    return "I'm not sure I understand. Can you try rephrasing?"
    

           

if __name__ == "__main__":
    
    #engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    # Define query groups
    
    wishMe()
    while True:
        query = command().lower()
        # query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("today's schedule" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("open google" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()
         # Check query and respond
        else:
            # Call classify_and_respond function for all other inputs
            response = classify_and_respond(query, tokenizer, model, label_encoder)
            speak(response)

       
        




