Traffic_Trade
Traffic_Trade is a hybrid computer vision and embedded systems project designed to automate traffic signal control using real-time vehicle detection. It combines Computer Vision with Arduino-driven traffic light control to simulate adaptive traffic systems.

Notable Techniques:

1) Object Detection: Vehicle detection is utilizing PyTorch under the hood for efficient inference on both images and videos.
2)Serial Communication: Uses pyserial to send different signal durations from Python to an Arduino board over USB.
3) Video Frame Annotation: OpenCV is used extensively to draw bounding boxes, labels, and overlays on image and video frames.
4) Machine Learning: A ML model ws trained using referenced datasets to use in the project.
5) CSV Logging: Real-time detections are logged using csv module for external analysis or future ML model training.
6) Multipoint Input Abstraction: Accepts input from static images (td1.py), webcam stream (td2.py), and video files (td3.py)—each following a uniform detection pipeline.

Libraries & Tools of Interest:

1)Ultralytics YOLOv5 – For vehicle detection.
2)OpenCV – Frame-by-frame processing and visualization.
3)PySerial – Communicates with Arduino devices.
4)Arduino IDE – Uploads the .ino file for controlling LEDs.

Directory Structure:

Traffic_Trade/
─ td1.py
─ td2.py
─ td3.py
─ FPupdated.ino
─ Videos/
─ output/
─ Traffic Trade/
─ README.md

Folders:
Videos: Input videos used for traffic analysis (td3.py)
output: Stores annotated frames or exported video with detection overlays
Traffic Trade: Contains the trained ML Model files

