init python:
    from chatgpt import *

    def character_image(emotion):
        if emotion is not None:
            return f"characters/main/{emotion}.png"
        else:
            return "characters/main/None.png"


define e = Character("AI")
image e = DynamicDisplayable(lambda st, at: (character_image(store.current_emotion), False))

image bg house = "places/house.jpg"
image bg default_place = "places/default.jpg"


label start:
    $ store.current_emotion = None
    scene bg house

    "You have a date."
    "Try to do your best! (template)"
    
    jump date

label date:
    $ end_date = False
    $ win_date = False
    $ time_passed = 0

    play music "audio/musics/main-ost.mp3" volume 0.4
    show bg default_place
    with fade
    show e
    with dissolve

    while not end_date:
        $ prompt = renpy.input("You:", length=100)

        show screen loading_points

        python:
            response = chat(prompt)
            store.chat_result = response

            # Check for end/win command
            if "*end*" in response.lower():
                store.current_emotion = "neutral"
                end_date = True
                if "*win*" in response.lower():
                    win_date = True

            # Character emotions
            emotion = emotions(response)
            if emotion is not None:
                store.current_emotion = emotion.lower()
            
            # TO DO: Day Night Cycle

        $ chat_result_formatted = dynamic_text_size(chat_result)
        hide screen loading_points

        show e
        e "[chat_result_formatted]"

        $ time_passed += 1
