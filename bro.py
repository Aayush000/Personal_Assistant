import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import random
import requests
from bs4 import BeautifulSoup
import sys
import cv2
import pywhatkit as kit
import pyautogui
import time

engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id) # (0th, 1st) index = (male, female) voice

def speak(audio):
    '''
    It converts the text into speech.
    '''
    engine.say(audio)
    engine.runAndWait()


def greetings():
    '''
    It activates your personal assistant.
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello, I am your personal assistant, but you can call me bro. I am here to help you, so what do you like me to do?")       

def takeCommand():
    '''
    It takes microphone input from the user and returns string output.
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("I did not get that. Can you please say that again...")  
        return "None"

    return query

def news():
    '''
    It helps to give the short description of four latest news.
    '''
    api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=bf652e8ec4e44d37b153eeec08507c74'
    main_page = requests.get(api_url).json()
    articles = main_page['articles']

    main_news = []
    position = ['first', 'second', 'third', 'fourth']
    
    for ar in articles:
        main_news.append(ar['title'])
    
    for i in range(len(position)):
        speak(f"Today's {position[i]} news is: {main_news[i]}")

def sendEmail(to, content):
    '''
    You have to 'enable the less secure apps' feature in your Gmail account. If you don't then sendEmail() might not work properly.
    '''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # server.login('real email id', 'your-password')
    # server.sendmail('real email id', to, content)
    server.login('testingassistant000@gmail.com', 'assistantTesting!')
    server.sendmail('testingassistant000@gmail.com', to, content)
    server.close()

def taskExecution():
    '''
    Execute different tasks.
    '''
    emails = {
        'email to danny':'person1@gmail.com',
        'email to sandy':'person2@gmail.com',
        'email to andy': 'person3@gmail.com',
        'email to john': 'person4@gmail.com'
    }

    greetings()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open calculator' in query:
            webbrowser.open("calculator.com")
        
        elif 'open twitter' in query:
            webbrowser.open("twitter.com")
        
        elif 'open facebook' in query:
            webbrowser.open("facebook.com")
        
        elif 'open instagram' in query:
            webbrowser.open("instagram.com")
        
        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")
        
        elif 'open calendar' in query:
            webbrowser.open("calendar.google.com")
        
        elif 'open map' in query:
            webbrowser.open("maps.google.com")
        
        elif 'open photo' in query:
            webbrowser.open("photos.google.com")

        elif 'open google' in query:
            speak('What do you like to search on google?')
            command = takeCommand().lower()
            webbrowser.open(f"{command}")
        
        elif 'play songs on youtube' in query:
            speak('Tell me the name of the song that you would like to hear.')
            command = takeCommand().lower()
            kit.playonyt(command)
        
        elif 'switch the window' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.keyUp('alt')

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   
        
        elif 'need a ride' in query:
            webbrowser.open(random.choice(['lyft.com', 'uber.com']))
        
        elif 'open command prompt' in query:
            os.system('start cmd')
        
        elif 'open notepad' in query:
            notepad_dir = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad.exe'
            os.startfile(notepad_dir)
        
        elif 'close notepad' in query:
            speak("Closing notepad...")
            os.system("taskkill/ f/ im notepad.exe")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\AppData\\Local\\Programs\\songs\\Top songs' # Insert the path to your music directory.
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, random.choice(songs)))
        
        elif 'open camera' in query:
            speak("Press q whenever you want to close the camera.")
            cam = cv2.VideoCapture(0)
            while True:
                ret, frame = cam.read()
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cam.release()
            cv2.destroyAllWindows()

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" # Insert the path to your visual studio code.
            os.startfile(codePath)
        
        elif 'close code' in query:
            speak("Closing visual studio code...")
            os.system("taskkill/ f/ im code.exe")
        
        elif 'shut down the computer' in query:
            os.system('shutdown /s')
        
        elif 'restart the computer' in query:
            os.system('shutdown /r')
        
        elif 'sleep the computer' in query:
            os.system('rundll32.exe powrprof.dll, SetSuspendState Sleep')
        
        elif 'tell me news' in query:
            speak('Sure. Give me a moment to fetch the latest news.')
            news()
        
        elif "what's my location" in query:
            speak("Let me check...")

            try:
                ip_address = requests.get('https://api.ipify.org/').text
                url = "https://get.geojs.io/v1/ip/geo/" + ip_address + ".json"
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                region = geo_data['region']
                country = geo_data['country']
                speak(f"I am not totally sure; however, I think you are in {region} in {country}")
            except Exception as e:
                speak("I was unable to find your location. sorry!")

        elif 'take screenshot' in query:
            speak("Can you please tell me the name for your screenshot file?")
            name = takeCommand().lower()
            speak("Please hold the screen for 3 seconds. I am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak(f"Screenshot is saved in the main folder with the name {name}")

        elif 'temperature' in  query:
            search = 'temperature in nashville'
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"current {search} is {temp}")
        
        for person in ['email to danny', 'email to sandy', 'email to andy', 'email to john']:
            if person in query:
                try: 
                    speak("What should I say?")
                    content = takeCommand()
                    to = emails[person]   
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry sir. I am not being able to send this email")
        
        if 'hello' in query or 'hey' in query:
            speak("Hello sir, how can I help you?")
        
        elif 'how are you' in query:
            speak("I am fine sir, how about you?")
        
        elif 'fine' in query or 'also good' in query or 'also doing well' in query:
            speak("That's awesome")

        elif 'thank you' in query or 'thanks' in query:
            speak("It's my pleasure.")
        
        elif 'you can sleep' in query or 'sleep now' in query:
            speak('Sure sir. I am going to sleep for now, but you can call me anytime.')
            break


if __name__ == "__main__":
    while True:
        permission = takeCommand()
        if "wake up" in permission:
            taskExecution()
        elif "goodbye" in permission:
            speak("Thanks for using me. You have a good day sir.")
            sys.exit()