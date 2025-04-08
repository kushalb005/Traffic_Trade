import cv2
import torch
import time
import csv
import os
from datetime import datetime
from ultralytics import YOLO

model = YOLO("models/yolov5s.pt")
input_video = "Videos/test1.mp4" 
output_video = "output_video.mp4"

cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, (200, 200))


VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
csv_file = "vehicle_data.csv"

if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Vehicle Type", "X1", "Y1", "X2", "Y2", "Confidence"])

def save_vehicle_data(vehicle_type, x1, y1, x2, y2, confidence):
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), vehicle_type, x1, y1, x2, y2, confidence])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (800, 800))

    results = model(frame)
    vehicle_count = 0

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            if class_id in VEHICLE_CLASSES:
                vehicle_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = round(float(box.conf[0]), 2)
                vehicle_type = VEHICLE_CLASSES[class_id]

                save_vehicle_data(vehicle_type, x1, y1, x2, y2, confidence)
                label = f"{vehicle_type} ({confidence})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Live Vehicle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print(f"Vehicle detection complete.")
