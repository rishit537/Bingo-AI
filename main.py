import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
wake_word = "bingo"
newsapi = "c1e8ed90a395416da7e4da978a95129f"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Bingo skilled in general tasks like Alexa and Google Cloud. Give short responses. Do not highlight parts of content with special characters. Example, '*The Weeknd* is a singer' is wrong. Just say, 'The Weeknd is a singer'. Also do not use special characters for bullet points.",
            },
            {"role": "user", "content": command},
        ],
    )
    return response.choices[0].message.content


def processCommand(c):
    if c.lower().startswith("open"):
        site = c.lower().replace("open ", "")
        if site == "google":
            webbrowser.open("https://google.com")
        elif site == "facebook":
            webbrowser.open("https://facebook.com")
        elif site == "youtube":
            webbrowser.open("https://youtube.com")
        elif site == "instagram":
            webbrowser.open("https://instagram.com")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "")
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        speak("Here's some news:")
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])[:5]
            for article in articles:
                print(article["title"])
                speak(article["title"])

    else:
        # let deepseek handle the request
        speak(aiProcess(c))
        print(aiProcess(c))


if __name__ == "__main__":
    speak("Initializing Bingo...")
    while True:
        # * Listen for the wake word 'Bingo'

        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing")
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            # Recognising wake word
            if word.lower() == wake_word:
                speak("Yes")

                # Listen for command
                with sr.Microphone() as source:
                    print("Bingo active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))
