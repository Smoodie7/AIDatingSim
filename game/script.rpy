init python:
    from chatgpt import *

    valid_places = ("cafe", "park")

    def character_image(emotion):
        if emotion is not None:
            return f"characters/main/{emotion}.png"
        else:
            return "characters/main/None.png"


define e = Character("AI")
image e = DynamicDisplayable(lambda st, at: (character_image(store.current_emotion), False))


label start:
    $ store.current_emotion = None
    scene bg "places/house.jpg"

    "You have a date."
    "Try to do your best! (template)"
    
    jump date

label date:
    $ end_date = False
    $ win_date = False
    $ time_passed = 0

    play music "audio/musics/main-ost.mp3" volume 0.4
    scene bg "places/default.jpg"
    with fade
    show e
    with dissolve

    while not end_date:
        $ prompt = renpy.input("You:", length=100)

        show screen loading_points

        python:
            try:
                response = chat(prompt)
            except Exception as exception:
                # NOT WORKING : Condition
                if Exception == 429:
                    response = "*sad*, oh sorry, but you reached the rate limit on requests! Your answering too fast (Limit 3 / min, 429 Error.)"
                response = "*sad*, oh oh something wrent wrong! I cant connect to reply you. Maybe you should verify your connection or take a look at 'log.txt."
                print("! Failed to get answer from chat() function, maybe you should check your internet connection?\n", exception)

            # Initialize place_name
            place_name = None


            # Check for ai command and emotions
            current_commands = re.findall(r'\*(.*?)\*', response.lower())
            if current_commands:
                current_emotion = emotions(current_commands)
                    
                print("> Commands or Emotions Detected:", current_commands)
                for current_command in current_commands:
                    if "end" in current_command or "win" in current_command:
                        current_emotion = "neutral"
                        end_date = True
                        print("> Date End:", end_date)
                        if "win" in current_command:
                            win_date = True
                    
                    elif "place" in current_command:
                        for valid_place in valid_places:
                            if re.search(r'\b{}\b'.format(valid_place), current_command):
                                current_place = valid_place
                                print("> TP to:", current_place)
                            
                                
            
        # TO DO: Day Night Cycle

        $ chat_result_formatted = dynamic_text_size(response)
        hide screen loading_points

        if place_name:
            scene bg [current_place]
        show e
        
        e "[chat_result_formatted]"

        $ time_passed += 1
