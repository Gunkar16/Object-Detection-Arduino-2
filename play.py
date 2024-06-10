from gtts import gTTS
import os
import argparse
from collections import Counter
import pygame

def pluralize(word, count):
    if count == 1:
        return word
    if word.endswith("s") or word.endswith("x") or word.endswith("ch") or word.endswith("sh"):
        return word + "es"
    elif word.endswith("y"):
        return word[:-1] + "ies"
    else:
        return word + "s"

def translate_detection_results(detection_results):
    # Count the occurrences of each detected object
    object_counts = Counter(detection_results)
    
    # Generate the translated message
    count = sum(object_counts.values())
    if detection_results == ['']:
        message = "Sorry, I cannot see anything here."
    else:
        # Sort the items based on their count in descending order
        object_count_items = sorted(object_counts.items(), key=lambda item: item[1], reverse=True)
        
        if count == 1:
            message = "There is "
            obj = next(iter(object_counts))
            message += f"1 {obj} in front of you."
        else:
            message = "There "
            # Handle the case for mixed singular and plural objects
            is_plural = any(cnt > 1 for cnt in object_counts.values())
            if is_plural:
                message += "are "
            else:
                message += "is "
            
            for i, (obj, count) in enumerate(object_count_items):
                obj_plural = pluralize(obj, count)
                if count == 1:
                    message += f"1 {obj}"
                else:
                    message += f"{count} {obj_plural}"
                if i < len(object_count_items) - 2:
                    message += ", "
                elif i == len(object_count_items) - 2:
                    message += " and "
            message += " in front of you."
    
    return message

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Translate detection results into spoken English.")
    parser.add_argument("detection_results", nargs="+", help="List of detected objects")
    args = parser.parse_args()

    # Translate detection results into spoken English
    translated_message = translate_detection_results(args.detection_results)

    # Convert text to speech
    tts = gTTS(translated_message)

    # Save the speech as a temporary file
    speech_file = "translated_speech.mp3"
    tts.save(speech_file)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the speech
    pygame.mixer.music.load(speech_file)
    pygame.mixer.music.play()

    # Wait for the speech to finish playing
    while pygame.mixer.music.get_busy():
        continue

