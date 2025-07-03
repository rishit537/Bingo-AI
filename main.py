import os
import warnings

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

import ast
import pygame
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import aiProcessing as ap
import edge_tts
import asyncio

recognizer = sr.Recognizer()
engine = pyttsx3.init()
# voices = engine.getProperty("voices")
wake_word = "bingo"
newsapi = "c1e8ed90a395416da7e4da978a95129f"

# for voice in voices:
#     if "male" in voice.name.lower():
#         engine.setProperty("voice", voice.id)
#         break

engine.setProperty("rate", 150)


async def speak(text):
    # engine.say(text)
    # engine.runAndWait()
    tts = edge_tts.Communicate(text=text, voice="en-US-GuyNeural")
    await tts.save("output.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    pygame.quit()
    os.remove("output.mp3")


def processCommand(c):
    req = ast.literal_eval(ap.aiProcess(c, "process"))
    category = req[0]
    if category == "website":
        site = req[1]
        webbrowser.open(site)

    elif category == "music":
        song = req[1]
        link = musicLibrary.music[song]
        asyncio.run(speak(f"Playing {song}"))
        webbrowser.open(link)

    elif category == "news":
        asyncio.run(speak("Here's some news:"))
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])[:5]
            for article in articles:
                print(article["title"])
                asyncio.run(speak(article["title"]))

    else:
        # let OpenAI handle the request
        response = ap.aiProcess(c)
        print(response)
        asyncio.run(speak(response))


if __name__ == "__main__":

    asyncio.run(speak("Initializing Bingo..."))
    while True:
        # * Listen for the wake word 'Bingo'

        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing")
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=None, phrase_time_limit=1.2)
            word = r.recognize_google(audio)
            # Recognising wake word
            if word.lower() == wake_word:

                # Listen for command
                with sr.Microphone() as source:
                    asyncio.run(speak("Yes"))
                    print("Bingo active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))
