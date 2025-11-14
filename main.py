import os
import threading
import warnings

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

import ast
import pygame
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from aiProcessing import aiProcess
from spotify import *
import edge_tts
import asyncio
from dotenv import load_dotenv


# Load the environment variables
load_dotenv("./.env")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
wake_word = "bingo"
NEWSAPI = os.environ.get("NEWS_API")
OPENAI_API = os.environ.get("OPENAI_API")

engine.setProperty("rate", 150)


def playsound(path, wait=False):
    def _play():
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        pygame.quit()

    if wait:
        _play()
    else:
        threading.Thread(target=_play, daemon=True).start()


async def speak(text):
    # engine.say(text)
    # engine.runAndWait()
    tts = edge_tts.Communicate(text=text, voice="en-US-GuyNeural")
    await tts.save("output.mp3")
    print(text)
    playsound("output.mp3", True)
    os.remove("output.mp3")


def processCommand(c):
    req = ast.literal_eval(aiProcess(OPENAI_API, c, "process"))
    category = req[0]
    if category == "website":
        site = req[1]["url"]
        query = req[1]["query"]
        if query != "":
            if site == "https://google.com":
                webbrowser.open(f"{site}/search?q={query}")
                asyncio.run(
                    speak(f"Opening Google on your browser to search for {query}...")
                )
            elif site == "https://youtube.com":
                webbrowser.open(f"{site}/results?search_query={query}")
                asyncio.run(
                    speak(f"Opening YouTube on your browser to search for {query}...")
                )
        else:
            webbrowser.open(site)

    elif category == "spotify":
        track = req[1]["track"]
        artist = req[1]["artist"]
        album = req[1]["album"]
        playlist = req[1]["playlist"]
        shuffle = req[1]["shuffle"]
        repeat = req[1]["repeat"]
        searchSpotify(track, artist, album, playlist, shuffle, repeat)

    elif category == "news":
        if NEWSAPI:
            asyncio.run(speak("Here's some news:"))
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI}"
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])[:5]
                for article in articles:
                    asyncio.run(speak(article["title"]))
        else:
            print("Error: NewsAPI API Key not found")
            print(
                "Please make sure you have included your NEWS_API Api Key in the .env file to access this feature"
            )

    else:
        # let OpenAI handle the request
        response = aiProcess(OPENAI_API, c)
        asyncio.run(speak(response))


if __name__ == "__main__":

    asyncio.run(speak("Initializing Bingo..."))
    # * Listen for the wake word 'Bingo'

    r = sr.Recognizer()
    r.energy_threshold = 350
    # obtain audio from the microphone

    with sr.Microphone() as source:
        # recognize speech using Google
        while True:
            print("Listening...")
            r.pause_threshold = 0.8  # silence timeout after user finishes speaking
            try:
                audio = r.listen(source, timeout=None)
                word = r.recognize_google(audio)

                # Recognising wake word
                if wake_word in word.lower():
                    r.pause_threshold = (
                        1.7  # silence timeout after user finishes speaking
                    )
                    # Listen for command
                    playsound("start_listening.mp3")
                    print("Bingo active...")
                    audio = r.listen(source, phrase_time_limit=10)
                    playsound("finish_listening.mp3")
                    command = r.recognize_google(audio)
                    processCommand(command)
            except Exception as e:
                print("Error: {0}".format(e))
