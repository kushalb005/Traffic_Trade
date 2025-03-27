import cv2
import torch
import os
import time
import serial 
from ultralytics import YOLO

# ser = serial.Serial('COM3', 9600, timeout=1)
model = YOLO("models/yolov5s.pt")
image_paths = {
    "north": "F:\FP\Videos\Screenshot 2025-03-27 004141.png",
    "south": "F:\FP\Videos\Screenshot 2025-03-27 004239.png",
    "east": "F:\FP\Videos\Screenshot 2025-03-27 004337.png",
    "west": "F:\FP\Videos\Screenshot 2025-03-27 004437.png"
}
vehicle_counts = {}
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

def calculate_green_time(vehicle_count):
    min_time = 10  
    max_time = 120
    factor = 3      
    
    green_time = min_time + (vehicle_count * factor)
    return max(min_time, min(green_time, max_time))  

for direction, image_path in image_paths.items():
    if not os.path.exists(image_path):
        print(f"Image for {direction} not found!")
        continue
    img = cv2.imread(image_path)

    results = model(img)

    vehicle_count = 0  

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  
            if class_id in VEHICLE_CLASSES:
                vehicle_count += 1 
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{VEHICLE_CLASSES[class_id]}"

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    vehicle_counts[direction] = vehicle_count
    green_time = calculate_green_time(vehicle_count)
    cv2.putText(img, f"Vehicles: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img, f"Green Time: {green_time}s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    output_path = f"output/{direction}_output.jpg"
    cv2.imwrite(output_path, img)

    print(f"{direction.upper()} → Vehicles: {vehicle_count}, Green Time: {green_time}s")
    
    # ser.write(str(green_time).encode())  
    # time.sleep(1) 
with open("vehicle_counts.txt", "w") as f:
    for direction, count in vehicle_counts.items():
        f.write(f"{direction}: {count}\n")

print("✅ Vehicle counts saved to 'vehicle_counts.txt'!")
