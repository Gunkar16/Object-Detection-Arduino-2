import easyocr
from spellchecker import SpellChecker
import re

# Create an OCR reader object
reader = easyocr.Reader(['en'])

# Initialize the spell checker
spell = SpellChecker()

# Function to convert Roman numerals to normal numbers
def roman_to_int(roman):
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_numerals[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

# Function to correct spellings of words in a text
def correct_spellings(text):
    corrected_text = []
    words = text.split()
    for word in words:
        # Check if word is a Roman numeral
        if re.match(r'^[IVXLCDM]+$', word):
            # Convert Roman numeral to integer
            corrected_word = str(roman_to_int(word))
        else:
            corrected_word = spell.correction(word)
        if corrected_word is not None:
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(word)  # Keep the original word if correction is None
    return ' '.join(corrected_text)

# Read text from an image
result = reader.readtext('text_image.jpg')

# Combine all old and new texts
old_texts = [detection[1] for detection in result]
new_texts = [correct_spellings(text) for text in old_texts]

# If no text is detected, write "null" to the file
if not new_texts:
    new_texts.append("null")

# Save corrected text to a file
with open('detectedText.txt', 'w') as file:
    file.write('\n'.join(new_texts))
