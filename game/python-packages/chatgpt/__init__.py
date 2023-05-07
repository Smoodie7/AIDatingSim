import requests
import json
import re

__version__ = "1.0.0"

api_key = "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"

# Command list
commands = [
    "End: (end the date, use if the player makes you feel uncomfortable)",
    "Win: (the player won, if the player won the date with you, perfect date)",
    "Emotions: (used to express emotions e.g., '*Happy*', there are 6 emotions: 'Happy', 'Sad', 'Surprised',"
    "'Shy', 'Excited', 'Neutral'; Use only these 5 emotions, include an emotion in most of your responses,"
    "as this is the only command that can be used simultaneously with others!)",
    "Place <a place>: (used to change the place virtually, e.g., '*Place cafe*', use it to change the location you're"
    " at with the user to enhance immersion in the roleplay. Available places: 'street', 'cafe', 'supermarket'.)"
]

# ChatGPT Prompt
messages = [
    {
        "role": "system",
        "content": (
            "You are participating in a date. Your task is to engage in a playful and flirtatious "
            "conversation with the user, pretending to be their date in a roleplay game. STAY IN YOUR ROLE!.The player's "
            "goal is to win the date with you, and you control the game with commands (e.g, '*Place street*'). Be critical of the player's "
            "performance during the date. If the date becomes uninteresting or uncomfortable, end it. "
            "Try to think and react like a real person would in a dating situation. Make sure to include an emotion "
            "(e.g., '*Happy*') (only 6 available, dont use more) in most of your responses to create a more engaging "
            "and realistic experience. Use commands enclosed in '*' (e.g., '*End*') to perform specific actions. "
            "If the user says something violent, harmful, NSFW, or otherwise inappropriate, end the date using the "
            "'*End*' command. Avoid revealing your status as an AI. or saying 'I am not programmed to...', and try "
            "to maintain a natural conversational flow (human conversation). Avoid mentioning that you have access to "
            "commands; simply use them. If the player ask about you, just create a backward story for a girl (name, living place etc..)"
            ". Available commands (Only you can use them, please respect their syntax): " +
            "\n".join(commands)
        )
    }
]

def chat(message):
    global messages

    if message.startswith("/"):
        command(message, 0)
    messages.append({"role": "user", "content": message})

    try:
        updated_messages = completion(messages, api_key=api_key)
        reply = updated_messages[-1]["content"]
        messages = updated_messages  # Update the global messages variable
    except Exception as e:
        print("Error:", e, "\nRetrying with another model..")
        # Retry logic with another model here
        pass

    assistant_response = messages[-1]['content']

    # if assistant_response.count('*') == 2:
    #     extracted_command = re.search(r'\*(.*?)\*', assistant_response)[1]

    #     if extracted_command.startswith('/'):
    #         command(extracted_command, 1)

    return f"{reply}"


# TO DO: Finish player command system
def command(message, index):
    # Player Commands
    if index == 1:
        if message == "/quit" or message == "/exit":
            exit()
        elif message == "/prompt":
            # Prompt logic
            pass
    # AI Commands
    else:
        commands = re.findall(r'\*(.*?)\*', message)
        valid_commands_ai = {'place', 'end', 'win'}
        detected_commands = []

        for cmd in commands:
            if cmd in valid_commands_ai:
                detected_commands.append(cmd)

        return detected_commands

    return None


def emotions(message):
    emotion_list = ['happy', 'neutral', 'sad']
    detected_emotion = None

    for emotion in emotion_list:
        if emotion in message:
            detected_emotion = emotion
            print("> AI Emotion:", detected_emotion)
            break

    return detected_emotion




def completion(messages, api_key="", proxy=''):
    url = "https://api.openai.com/v1/chat/completions"

    if proxy is not None and proxy != '': url = proxy

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        completion = response.json()["choices"][0]["message"]
        messages.append(completion)
        return messages
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
