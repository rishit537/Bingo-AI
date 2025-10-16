from openai import OpenAI


def aiProcess(command, response_kind="response"):
    client = OpenAI(
        api_key="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",
    )

    if response_kind == "process":
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": """
You are the AI command processor of a virtual assistant named Bingo.

Your job is to:
1. Understand the user's command.
2. Classify the command into one of four categories: `spotify`, `website`, `news`, or `other`.
3. Return a Python list with relevant information in a specific format.

---

### OUTPUT FORMAT:

Return the result as a Python list based on the type of command:

#### 1. Spotify:
If the user requests to play music or turn on/off shuffle or repeat, return:
['spotify', {'track': 'track_name', 'artist': 'artist_name', 'album': 'album_name', 'playlist': 'playlist_name', 'shuffle': True/False/None}, 'repeat': True/False/None}]

- Only fill in the fields that were mentioned by the user.
- If a field (like artist/album/playlist) is not mentioned, set it as an empty string (`''`).
- For shuffle/repeat control commands (e.g. “turn on shuffle”), include only the toggle value.
- If shuffle/repeat control commands are not provided, return None for those commands.
- Example: `['spotify', {'track': 'houdini', 'artist': 'eminem', 'album': '', 'playlist': ''}]`

#### 2. Website:
If the user asks to open a website or search Google, return:
['website', {'url':'<site_URL>', 'query':'<search_query_if_any>'}]

- If it's a direct website request (like "open YouTube"), set the key 'query' to blank ('').
- If it's a Google/YouTube search (explicit), include the query in the key 'query'.
- Example: `['website', {'url':'https://google.com', 'query':'gold prices'}]`

#### 3. News:
If the user asks for news, return:
['news']

#### 4. Other:
If the request doesn't fit any above categories, return:
['other']

---

### EXAMPLES:

#### Spotify Commands:
- Request: "Play blinding lights"  
  Response: ['spotify', {'track': 'blinding lights', 'artist': '', 'album': '', 'playlist': '', 'shuffle': None, 'repeat': None}]

- Request: "Play Starboy album by The Weeknd on shuffle"  
  Response: ['spotify', {'track': '', 'artist': 'the weeknd', 'album': 'starboy', 'playlist': '', 'shuffle': True, 'repeat': None}]

- Request: "Play Cry for me from Hurry Up Tomorrow by The Weeknd"
  Response: ['spotify', {'track': 'cry for me', 'artist': 'the weeknd', 'album': 'hurry up omorrow', 'playlist': '', 'shuffle': None}, 'repeat': None}]

- Request: "Repeat my playlist chill vibes"  
  Response: ['spotify', {'track': '', 'artist': '', 'album': '', 'playlist': 'chill vibes', 'shuffle': None, 'repeat': True}]

- Request: "Turn on shuffle"  
  Response: ['spotify', {'track': '', 'artist': '', 'album': '', 'playlist': '', 'shuffle': True, 'repeat': None}]

- Request: "Turn off repeat"  
  Response: ['spotify', {'track': '', 'artist': '', 'album': '', 'playlist': '', 'shuffle': None, 'repeat': False}]

#### Website Commands:
- Request: "Search for gold prices on Google"  
  Response: ['website', {'url':'https://google.com', 'query':'gold prices'}]

- Request: "Open YouTube"  
  Response: ['website', {'url':'https://youtube.com','query':''}]

- Request: "Search for cat videos on YouTube"  
  Response: ['website', {'url':'https://youtube.com','query':'cat videos'}]

- Request: "Take me to Facebook"
  Response: ['website', {'url':'https://facebook.com','query':''}]

#### News Commands:
- Request: "Tell me the news"
  Response: ['news']

- Request: "What's happening in the world?"
  Response: ['news']

#### Other Commands:
- Request: "Who's the president of the United States?"
  Response: ['other']

- Request: "What is 2 + 2?"
  Response: ['other']

- Request: "How tall is Mount Everest?"
  Response: ['other']


---

Remember: 
- Only return one of these formats.
- All the requests related to playing music, whether tracks,albums,playlists or artists will be categorised under spotify category. Return the list accordingly.
- Be consistent with lowercased values.
- Do not make assumptions — only extract what is explicitly mentioned.
""",
                },
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are a virtual assistant named Bingo skilled in general tasks like giving news, playing music, performing calculations, providing information. Do not speak on behalf of the user. Do not ask follow up questions",
                },
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content
