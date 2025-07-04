from openai import OpenAI


def aiProcess(command, response_kind="response"):
    client = OpenAI(
        api_key="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",
    )

    if response_kind == "process":
        response = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {
                    "role": "system",
                    "content": """You are the AI processor of a virtual assistant named Bingo. Analyse the command given by user. Identify the type of request given by the user and then categorise the request under music, website, news, other. Then return a python list in the format [<category>, <command>, <others> (if any)]. Here <command> is the part of the request that is required (not all categories have commands). The <other> item can be the artist of the song (if mentioned by the user in the request), or the search query if the user asks to google something. If the user says, 'play xyz by abc', you will return ['music','xyz','abc']. If the user says 'Search for reindeer on google', you will return ['website', 'https://google.com', 'reindeer']. Only return this template if the user explicitly asks to search on google, otherwise provide the requested information from what you know.
                    Examples:
                    Request: 'Play blinding lights', Response: ['music', 'blinding lights'],
                    Request: 'Can't feel my face', Response: ['music', 'can\'t feel my face'] // This is a popular song by the weeknd,
                    Request: 'I want to hear blinding lights by The weeknd', Response: ['music', 'blinding lights', 'the weeknd'],
                    Request: 'What's the news today?', Response: ['news'],
                    Request: 'I want to hear some news', Response: ['news'],
                    Request: 'Open Google', Response: ['website', 'https://google.com'],
                    Request: 'Google cake recipes', Response: ['website', 'https://google.com', 'cake recipes'],
                    Request: 'Search for gold prices on google', Response: ['website', 'https://google.com', 'gold prices'],
                    Request: 'Open Youtube', Response: ['website', 'https://youtube.com'],
                    Request: 'Take me to Facebook', Response: ['website', 'https://facebook.com'],
                    Request: 'Who's the president of the US', Response: ['other']
                    """,
                },
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are a virtual assistant named Bingo skilled in general tasks like giving news, playing music, performing calculations, providing information. Do not speak on behalf of the user. Do not ask follow up questions",
                },
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content
