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
                    "content": """You are the AI processor of a virtual assistant named Bingo. Analyse the command given by user. Identify the type of request given by the user and then categorise the request under music, website, news, other. Then return a python list in the format [<category>, <command>]. Here <command> is the part of the request that is required (not all categories have commands). The speech recognition software might not recognise the commands of user correctly, for example, the user might say 'blinding lights' and the speech recognition software might hear 'blinding light'. So as an AI, use your intelligence to understand user's request. In this specific example, correct it to 'blinding lights' and then continue the task.
                    Examples:
                    Request: 'Play blinding lights', Response: ['music', 'blinding lights'],
                    Request: 'Can't feel my face', Response: ['music', 'can\'t feel my face'] // This is a popular song by the weeknd,
                    Request: 'I want to hear blinding lights', Response: ['music', 'blinding lights'],
                    Request: 'What's the news today?', Response: ['news'],
                    Request: 'I want to hear some news', Response: ['news'],
                    Request: 'Open Google', Response: ['website', 'https://google.com'],
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
