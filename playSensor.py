from gtts import gTTS
from playsound import playsound
import os

if __name__ == "__main__":
    # Read text from detectedText.txt
    with open('detectedText.txt', 'r') as file:
        text = file.read().strip()

    # Check if the text contains the word 'null'
    if 'null' in text.lower():
        # If 'null' is found, dictate "Sorry, I cannot see anything here."
        text_to_speak = "Sorry, I cannot see anything here."
    else:
        # Convert text to speech
        tts = gTTS(text)
        # Save the speech as a temporary file
        speech_file = "detectedText.mp3"
        tts.save(speech_file)
        # Play the speech
        playsound(speech_file)
        # Remove the temporary file
        os.remove(speech_file)
