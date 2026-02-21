import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import time
import webbrowser
import os

ASSISTANT_NAME = "Jarvis"
USER_NAME = "Adeel"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


def speak(text):
    if not text:
        return

    engine.stop()  
    engine.say(text)
    engine.runAndWait()

    while engine.isBusy():
        time.sleep(0.1)


def greet_user():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # Queue both sentences before running
    engine.say(f"{greeting} {USER_NAME}.")
    engine.say(f"I am {ASSISTANT_NAME}. How can I help you today?")
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print("You said:", query)
        return query.lower()

    except sr.UnknownValueError:
        speak("I did not understand that.")
        return ""

    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

def search_wikipedia(query):
    try:
        topic = query.replace("wikipedia", "").strip()

        if not topic:
            speak("What should I search on Wikipedia?")
            return

        speak("Searching Wikipedia...")
        result = wikipedia.summary(topic, sentences=2)

        print(result)

        time.sleep(0.5)

        engine.say("According to Wikipedia.")
        engine.say(result[:600])  
        engine.runAndWait()

    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")

    except wikipedia.exceptions.PageError:
        speak("I could not find anything on Wikipedia.")

    except Exception as e:
        print("Wikipedia error:", e)
        speak("Something went wrong while searching.")


def main():
    greet_user()

    while True:
        query = listen()

        if not query:
            continue

        if "wikipedia" in query:
            search_wikipedia(query)
        elif "open google" in query:
            webbrowser.open("https://www.google.com/")
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com/")
        elif "open facebook" in query:
            webbrowser.open("https://www.facebook.com/")
        elif "open linkedin" in query:
            webbrowser.open("https://www.linkedin.com/home?originalSubdomain=pk") 
        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye.") 
            break 
        elif "play music" in query:
            music_directory = "C:\\Users\\786\\Music"
            songs = [f for f in os.listdir(music_directory) if f.endswith(('.mp3', '.wav'))]
            if songs:
                song = os.path.join(music_directory, songs[0])
                speak("Playing music...")
                os.startfile(song)
            else:
                speak("No music files found in the directory.")

if __name__ == "__main__":
    main()