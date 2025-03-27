import torch
import cv2
import time
import numpy as np
import serial  
from ultralytics import YOLO

#ser = serial.Serial('COM3', 9600, timeout=1)  

model = YOLO("yolov5s.pt")

input_video = "Videos/test1.mp4"   
output_video = "output_video.mp4"
cap = cv2.VideoCapture(input_video)
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, (200, 200))
vehicle_classes = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

def calculate_green_time(vehicle_count):
    min_time = 10   
    max_time = 120   
    factor = 3     
    green_time = min_time + (vehicle_count * factor)
    green_time = max(min_time, min(green_time, max_time))
    
    return int(green_time)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (800, 800))
    results = model(frame, stream=True)

    vehicle_count = 0  

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])  
            if cls in vehicle_classes:
                vehicle_count += 1 
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])  

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{vehicle_classes[cls]} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    green_time = calculate_green_time(vehicle_count)

    cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, f"Green Time: {green_time}s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # ser.write(str(green_time).encode())  
    # time.sleep(1) 

    out.write(frame)
    cv2.imshow("Vehicle Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
#ser.close()  # Close Serial Communication

print(f"✅ Vehicle detection complete. Output saved as {output_video}")
