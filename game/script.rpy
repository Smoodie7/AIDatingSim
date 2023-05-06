init python:
    from chatgpt import *

define e = Character("AI")

# The game starts here.
label start:

    $ end_date = False
    $ win_date = False

    show e happy
    scene bg room

    while not end_date:
        $ prompt = renpy.input("You:", length=100)

        show screen loading_points

        python:
            response = chat(prompt)
            store.chat_result = response

            # Check for the end command
            if "*end*" in response.lower():
                end_date = True
                if "*win*" in response.lower():
                    win_date = True

            emotion = emotions(response)
            if emotion is not None:
                store.current_emotion = emotion

        $ chat_result_formatted = dynamic_text_size(chat_result)
        hide screen loading_points

        e "[chat_result_formatted]"
        show e [emotion]



