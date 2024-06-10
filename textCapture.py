import cv2
import time

def capture_frame():
    # Open the webcam
    cap = cv2.VideoCapture(1)  # Use index 1 for the second webcam if needed

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    # Start time
    start_time = time.time()

    # Loop to continuously read and display frames from the webcam for 5 seconds
    while (time.time() - start_time) < 3:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame is read correctly, display it
        if ret:
            cv2.imshow('Webcam', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Capture a frame before ending
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('text_image.jpg', frame)
        print("Frame captured successfully as 'text_image.jpg'.")

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to show the webcam stream for 5 seconds and capture a frame
capture_frame()
