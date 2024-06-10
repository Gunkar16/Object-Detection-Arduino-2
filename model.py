from ultralytics import YOLO
import torch

# Define the path to your image and model weight file
image_path = "captured_image.jpg"
model_path = "yolov8s.pt"  # Replace with your model weight file path

# Check if a GPU is available and set the device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

try:
    # Load the YOLOv8 model
    model = YOLO(model_path).to(device)

    # Perform object detection on the image
    results = model(image_path)

    # Extract class names and detected class indices
    class_names = results[0].names
    detected_classes = results[0].boxes.cls.to('cpu').tolist()
    detected_class_names = [class_names[class_index] for class_index in detected_classes]

    # Write the detection results and coordinates to files
    with open("detection_results.txt", "w") as result_file, open("detection_coordinates.txt", "w") as coord_file:
        result_file.write(",".join(detected_class_names))
        
        for box in results[0].boxes:
            class_index = box.cls.item()
            class_name = class_names[class_index]
            coordinates = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
            coord_file.write(f"{class_name},{coordinates[0]},{coordinates[1]},{coordinates[2]},{coordinates[3]}\n")

    print("Detection results written to detection_results.txt")
    print("Coordinates written to detection_coordinates.txt")

except Exception as e:
    print(f"An error occurred during model inference: {e}")
