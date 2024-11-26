#pip install wikipedia
#pip install pyaudio
#pip install pyttsx3
#pip install speechrecognition
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import re
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice to something more like JARVIS
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for a different voice
engine.setProperty('rate', 150)  # Adjust the speed of speech
engine.setProperty('volume', 1.0)  # Set volume level (0.0 to 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir!")
    else:
        speak("Good evening, sir!")
    speak("I am LOVELY KAUR. How can I assist you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Sorry, there was an issue with the request.")
            return "None"
    return query

def search_youtube(query):
    search_query = re.sub(r'\b(play|search|on)\b', '', query, flags=re.IGNORECASE).strip()
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)
    speak(f"Searching for {search_query} on YouTube")

def open_application(application):
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "microsoft edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        # Add more applications and their paths here
    }
    app = app_paths.get(application.lower(), None)
    if app:
        os.startfile(app)
        speak(f"Opening {application}")
    else:
        speak(f"Sorry, I couldn't find the application {application}")

if __name__== "__main__":
    wish_me()
    youtube_opened = False
    while True:
        query = take_command().lower()
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any results for that.")

        elif 'how are you' in query:
            speak("I am functioning optimally, sir.")

        elif 'what time is it' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}, sir.")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
            youtube_opened = True

        elif youtube_opened and ('play' in query or 'search' in query):
            search_youtube(query)
            youtube_opened = False

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif 'open github' in query:
            webbrowser.open("https://www.github.com")
            speak("Opening GitHub")

        elif 'search for' in query:
            search_query = query.replace("search for", "").strip()
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            speak(f"Searching for {search_query}")
        elif 'open' in query:
            application = query.replace('open', '').strip()
            open_application(application)

        elif 'exit' in query:
            speak("Goodbye, sir!")
            break