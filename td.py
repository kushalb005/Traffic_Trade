import cv2
import torch
import os
import time
import serial  # For ESP32 communication (optional)
from ultralytics import YOLO

# Initialize Serial Communication (Change COM Port if needed)
# ser = serial.Serial('COM3', 9600, timeout=1)

# Load YOLO model
model = YOLO("models/yolov5s.pt")

# Paths for input images (for each direction)
image_paths = {
    "north": "F:\FP\Videos\Screenshot 2025-03-27 004141.png",
    "south": "F:\FP\Videos\Screenshot 2025-03-27 004239.png",
    "east": "F:\FP\Videos\Screenshot 2025-03-27 004337.png",
    "west": "F:\FP\Videos\Screenshot 2025-03-27 004437.png"
}

# Vehicle count storage
vehicle_counts = {}

# Class IDs for cars, trucks, motorcycles, and buses (YOLO COCO dataset)
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

# Function to Calculate Green Signal Time
def calculate_green_time(vehicle_count):
    min_time = 10   # Minimum green light time (seconds)
    max_time = 120  # Maximum green light time
    factor = 3      # Scaling factor for traffic intensity
    
    green_time = min_time + (vehicle_count * factor)
    return max(min_time, min(green_time, max_time))  # Ensure within limits

# Process each direction
for direction, image_path in image_paths.items():
    if not os.path.exists(image_path):
        print(f"🚨 Image for {direction} not found!")
        continue

    # Read image
    img = cv2.imread(image_path)

    # Detect vehicles
    results = model(img)

    vehicle_count = 0  # Counter for detected vehicles

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get class ID
            if class_id in VEHICLE_CLASSES:
                vehicle_count += 1  # Count vehicle

                # Get bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{VEHICLE_CLASSES[class_id]}"

                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Store vehicle count for this direction
    vehicle_counts[direction] = vehicle_count

    # Calculate green signal time
    green_time = calculate_green_time(vehicle_count)

    # Display results on the image
    cv2.putText(img, f"Vehicles: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img, f"Green Time: {green_time}s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Save processed image
    output_path = f"output/{direction}_output.jpg"
    cv2.imwrite(output_path, img)

    print(f"{direction.upper()} → Vehicles: {vehicle_count}, Green Time: {green_time}s")
    
    # Send Green Time to ESP32 (if needed)
    # ser.write(str(green_time).encode())  
    # time.sleep(1)  # Small delay for stability

# Save vehicle counts to a file
with open("vehicle_counts.txt", "w") as f:
    for direction, count in vehicle_counts.items():
        f.write(f"{direction}: {count}\n")

print("✅ Vehicle counts saved to 'vehicle_counts.txt'!")
