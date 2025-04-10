<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>

  <h1>Traffic_Trade</h1>
  <p><strong>Traffic_Trade</strong> is a hybrid computer vision and embedded systems project designed to automate traffic signal control using real-time vehicle detection. It combines computer vision with Arduino-driven traffic light control to simulate adaptive traffic systems.</p>

  <h2>Notable Techniques</h2>
  <ul>
    <li><strong>Object Detection</strong>: Vehicle detection is utilizing PyTorch under the hood for efficient inference on both images and videos.</li>
    <li><strong>Serial Communication</strong>: Uses pyserial to send signal durations to Arduino.</li>
    <li><strong>Video Frame Annotation</strong>: Uses OpenCV to overlay bounding boxes and labels.</li>
    <li><strong>Machine Learning</strong>: Trained a custom YOLO model using vehicle datasets for inference.</li>
    <li><strong>CSV Logging</strong>: Detection results are written to CSV files for analysis or training reuse.</li>
    <li><strong>Multipoint Input Abstraction</strong>: Handles static images (<code>td1.py</code>), live webcam (<code>td2.py</code>), and video files (<code>td3.py</code>).</li>
  </ul>

  <h2>Libraries & Tools</h2>
  <ul>
    <li>Ultralytics YOLOv5 – For vehicle detection.</li>
    <li>OpenCV – Frame processing and annotations.</li>
    <li>PySerial – Communicates with Arduino via USB.</li>
    <li>Arduino IDE – Uploads .ino file to microcontroller.</li>
  </ul>

  <h2>Project Structure</h2>
  <pre>
Traffic_Trade/
─ td1.py
─ td2.py
─ td3.py
─ FPupdated.ino
─ Videos/
─ output/
─ Traffic Trade/
─ README.md
  </pre>

  <ul>
    <li><strong>Videos/</strong> – Input videos for demonstration</li>
    <li><strong>output/</strong> – Annotated output images and video exports</li>
    <li><strong>Traffic Trade/</strong> – Contains trained ML model files</li>
  </ul>

</body>
</html>
