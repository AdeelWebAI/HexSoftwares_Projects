import asyncio
import edge_tts
import speech_recognition as sr
import wikipedia
import datetime
import os
from playsound import playsound

# ==============================
# CONFIG
# ==============================
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Adeel"
VOICE = "en-US-GuyNeural"   # Change if you want

# ==============================
# EDGE TTS SPEAK FUNCTION
# ==============================
async def speak_async(text):
    if not text:
        return
    
    file_name = "voice.mp3"

    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(file_name)

    playsound(file_name)
    os.remove(file_name)


def speak(text):
    asyncio.run(speak_async(text))


# ==============================
# GREETING
# ==============================
def greet_user():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    speak(f"{greeting} {USER_NAME}.")
    speak(f"I am {ASSISTANT_NAME}. How can I help you today?")


# ==============================
# LISTEN FUNCTION
# ==============================
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


# ==============================
# WIKIPEDIA SEARCH
# ==============================
def search_wikipedia(query):
    try:
        topic = query.replace("wikipedia", "").strip()

        if not topic:
            speak("What should I search on Wikipedia?")
            return

        speak("Searching Wikipedia...")
        result = wikipedia.summary(topic, sentences=2)

        print(result)
        speak("According to Wikipedia.")
        speak(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")

    except wikipedia.exceptions.PageError:
        speak("I could not find anything on Wikipedia.")

    except Exception as e:
        print("Wikipedia Error:", e)
        speak("Something went wrong while searching.")


# ==============================
# MAIN LOOP
# ==============================
def main():
    greet_user()

    while True:
        query = listen()

        if not query:
            continue

        if "wikipedia" in query:
            search_wikipedia(query)

        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye.")
            break


if __name__ == "__main__":
    main() 