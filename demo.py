import subprocess
import threading
import pygame
import random
from gtts import gTTS
from playsound import playsound
import os
from collections import Counter
from ultralytics import YOLO
import torch

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Function to run a script and play sound simultaneously
def run_script_with_sound(script, sound_file):
    sound_thread = threading.Thread(target=play_sound, args=(sound_file,))
    script_thread = threading.Thread(target=subprocess.run, args=(['python', script],), kwargs={'check': True})
    
    # Start both threads
    sound_thread.start()
    script_thread.start()
    
    # Wait for both threads to complete
    sound_thread.join()
    script_thread.join()

# Function to generate a random color
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Dictionary to store colors for each class
class_colors = {}

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
    object_counts = Counter(detection_results)
    
    count = sum(object_counts.values())
    if detection_results == ['']:
        message = "Sorry, I cannot see anything here."
    else:
        object_count_items = sorted(object_counts.items(), key=lambda item: item[1], reverse=True)
        
        if count == 1:
            message = "There is "
            obj = next(iter(object_counts))
            message += f"1 {obj} in front of you."
        else:
            message = "There "
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

try:
    print("Starting the processes...")

    sound_thread = threading.Thread(target=play_sound, args=('image_capture.mp3',))
    capture_thread = threading.Thread(target=subprocess.run, args=(['python', 'capture.py'],), kwargs={'check': True})
    
    sound_thread.start()
    capture_thread.start()
    
    sound_thread.join()
    capture_thread.join()

    sound_thread = threading.Thread(target=play_sound, args=('image_processing.mp3',))
    model_thread = threading.Thread(target=subprocess.run, args=(['python', 'model.py'],), kwargs={'check': True})
    
    sound_thread.start()
    model_thread.start()
    
    sound_thread.join()
    model_thread.join()

    with open("detection_results.txt", "r") as f:
        detection_results = f.read().strip().split(',')

    play_thread = threading.Thread(target=subprocess.run, args=(['python', 'play.py'] + detection_results,), kwargs={'check': True})
    draw_thread = threading.Thread(target=subprocess.run, args=(['python', 'draw.py'] + detection_results,), kwargs={'check': True})
    
    play_thread.start()
    draw_thread.start()
    
    play_thread.join()
    draw_thread.join()

except subprocess.CalledProcessError as e:
    print(f"Subprocess error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("Processes completed.")
