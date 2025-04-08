import cv2
import torch
import os
import time
import serial  
from ultralytics import YOLO

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

model = YOLO("models/yolov5s.pt")
image_paths = {
    "north": "F:\FP\Videos\Screenshot 2025-03-27 004141.png",
    "south": "F:\FP\Videos\Screenshot 2025-03-27 004239.png",
    "east":  "F:\FP\Videos\Screenshot 2025-03-27 004337.png",
    "west":  "F:\FP\Videos\Screenshot 2025-03-27 004437.png"
}
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
VEHICLE_WEIGHTS = {"car": 1, "motorcycle": 1, "bus": 1, "truck": 1}

MIN_TIME = 10       
RIGHT_TURN_BUFFER = 3 
MAX_GREEN = 180       

vehicle_weighted = {}
vehicle_raw = {}
for direction, image_path in image_paths.items():
    if not os.path.exists(image_path):
        print(f"Image for {direction} not found!")
        continue

    img = cv2.imread(image_path)
    results = model(img)
    weighted_count = 0
    raw_count = 0

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            if class_id in VEHICLE_CLASSES:
                veh_type = VEHICLE_CLASSES[class_id]
                raw_count += 1
                weighted_count += VEHICLE_WEIGHTS[veh_type]

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, veh_type, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    vehicle_weighted[direction] = weighted_count
    vehicle_raw[direction] = raw_count

    if weighted_count == 0:
        green_time = MIN_TIME
    else:
        green_time = max(weighted_count, MIN_TIME) + RIGHT_TURN_BUFFER
    green_time = min(green_time, MAX_GREEN)
    
    cv2.putText(img, f"Vehicles: {raw_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img, f"Green Time: {green_time}s", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    output_path = f"output/{direction}_output.jpg"
    cv2.imwrite(output_path, img)

    print(f"{direction.upper()} -> Raw: {raw_count}, Weighted: {weighted_count}, Green Time: {green_time}s")

ns_weight = max(vehicle_weighted.get("north", 0), vehicle_weighted.get("south", 0))
if ns_weight == 0:
    ns_green = MIN_TIME
else:
    ns_green = max(ns_weight, MIN_TIME) + RIGHT_TURN_BUFFER
ns_green = min(ns_green, MAX_GREEN)

ew_weight = max(vehicle_weighted.get("east", 0), vehicle_weighted.get("west", 0))
if ew_weight == 0:
    ew_green = MIN_TIME
else:
    ew_green = max(ew_weight, MIN_TIME) + RIGHT_TURN_BUFFER
ew_green = min(ew_green, MAX_GREEN)

print(f"NORTH-SOUTH Group Green Time: {ns_green}s")
print(f"EAST-WEST Group Green Time: {ew_green}s")

signal_timing = f"{ns_green} {ew_green}\n"
print(f"Sending to ESP32: {signal_timing}")
ser.write(signal_timing.encode())
time.sleep(1)

with open("vehicle_counts.txt", "w") as f:
    for direction in image_paths.keys():
        raw = vehicle_raw.get(direction, 0)
        weighted = vehicle_weighted.get(direction, 0)
        f.write(f"{direction}: raw={raw}, weighted={weighted}\n")
print("Vehicle counts saved to 'vehicle_counts.txt'!")
