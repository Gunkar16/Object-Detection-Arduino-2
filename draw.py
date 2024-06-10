import cv2
import random

# Define the path to the image and the coordinates file
image_path = "captured_image.jpg"
coordinates_path = "detection_coordinates.txt"

# Load the image
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image")
    exit()

# Function to generate a random color
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Dictionary to store colors for each class
class_colors = {}

# Read the coordinates from the file
try:
    with open(coordinates_path, "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) != 5:
                continue
            class_name, x_min, y_min, x_max, y_max = parts
            x_min, y_min, x_max, y_max = map(float, [x_min, y_min, x_max, y_max])
            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
            
            # Get or assign a color for the class
            if class_name not in class_colors:
                class_colors[class_name] = get_random_color()
            color = class_colors[class_name]
            
            # Draw the bounding box
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
            # Put the class name label above the bounding box
            cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    # Save the output image (overwrite the original image)
    cv2.imwrite(image_path, image)
    print(f"Bounding boxes drawn on {image_path}")
except Exception as e:
    print(f"An error occurred while drawing bounding boxes: {e}")
