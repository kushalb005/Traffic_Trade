import torch
import cv2
import time
import numpy as np
import serial  # For ESP32 communication
from ultralytics import YOLO

# Initialize Serial Communication (Change COM Port if needed)
#ser = serial.Serial('COM3', 9600, timeout=1)  

# Load YOLO model
model = YOLO("yolov5s.pt")

# Define input and output video files
input_video = "Videos/test1.mp4"   # Change to your video file
output_video = "output_video.mp4"

# Open video capture
cap = cv2.VideoCapture(input_video)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define video writer to save output (200x200 resolution)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, (200, 200))

# Define vehicle classes from YOLO (COCO dataset)
vehicle_classes = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

# Function to Calculate Green Signal Time
def calculate_green_time(vehicle_count):
    min_time = 10   # Minimum green light time (in seconds)
    max_time = 120   # Maximum green light time (in seconds)
    factor = 3      # Scaling factor for traffic intensity
    
    # Calculate green light duration
    green_time = min_time + (vehicle_count * factor)
    
    # Ensure green_time is within limits
    green_time = max(min_time, min(green_time, max_time))
    
    return int(green_time)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to 200x200
    frame = cv2.resize(frame, (800, 800))

    # Run YOLO detection
    results = model(frame, stream=True)

    vehicle_count = 0  # Counter for detected vehicles

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])  # Get class index
            if cls in vehicle_classes:
                vehicle_count += 1  # Increment count
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])  # Confidence score

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{vehicle_classes[cls]} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Calculate green signal duration
    green_time = calculate_green_time(vehicle_count)

    # Display vehicle count and signal time
    cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, f"Green Time: {green_time}s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Send Green Time to ESP32
    # ser.write(str(green_time).encode())  
    # time.sleep(1)  # Small delay for communication

    # Write frame to output video
    out.write(frame)

    # Show frame (press "q" to exit)
    cv2.imshow("Vehicle Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
#ser.close()  # Close Serial Communication

print(f"✅ Vehicle detection complete. Output saved as {output_video}")
