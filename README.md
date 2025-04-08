<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Traffic_Trade</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 2rem;
      background-color: #f9f9f9;
      color: #333;
    }
    h1, h2 {
      color: #2c3e50;
    }
    code, pre {
      background-color: #eee;
      padding: 0.5rem;
      display: block;
      overflow-x: auto;
    }
    ul {
      padding-left: 1.5rem;
    }
    .folder-note {
      font-style: italic;
      color: #666;
    }
  </style>
</head>
<body>

  <h1>🚦 Traffic_Trade</h1>
  <p><strong>Traffic_Trade</strong> is a hybrid computer vision and embedded systems project designed to automate traffic signal control using real-time vehicle detection. It combines computer vision with Arduino-driven traffic light control to simulate adaptive traffic systems.</p>

  <h2>🛠️ Notable Techniques</h2>
  <ul>
    <li><strong>Object Detection</strong>: Vehicle detection is done using YOLOv5, leveraging <a href="https://pytorch.org/" target="_blank">PyTorch</a> for inference.</li>
    <li><strong>Serial Communication</strong>: Uses <a href="https://pythonhosted.org/pyserial/" target="_blank">pyserial</a> to send signal durations to Arduino.</li>
    <li><strong>Video Frame Annotation</strong>: Uses <a href="https://opencv.org/" target="_blank">OpenCV</a> to overlay bounding boxes and labels.</li>
    <li><strong>Machine Learning</strong>: Trained a custom YOLO model using vehicle datasets for inference.</li>
    <li><strong>CSV Logging</strong>: Detection results are written to CSV files for analysis or training reuse.</li>
    <li><strong>Multipoint Input Abstraction</strong>: Handles static images (<code>td1.py</code>), live webcam (<code>td2.py</code>), and video files (<code>td3.py</code>).</li>
  </ul>

  <h2>📦 Libraries & Tools</h2>
  <ul>
    <li><a href="https://github.com/ultralytics/yolov5" target="_blank">Ultralytics YOLOv5</a> – For vehicle detection.</li>
    <li><a href="https://opencv.org/" target="_blank">OpenCV</a> – Frame processing and annotations.</li>
    <li><a href="https://pythonhosted.org/pyserial/" target="_blank">PySerial</a> – Communicates with Arduino via USB.</li>
    <li><a href="https://www.arduino.cc/en/software" target="_blank">Arduino IDE</a> – Uploads <code>.ino</code> file to microcontroller.</li>
  </ul>

  <h2>📁 Project Structure</h2>
  <pre>
Traffic_Trade/
├── td1.py
├── td2.py
├── td3.py
├── FPupdated.ino
├── Videos/
├── output/
├── Traffic Trade/
└── README.md
  </pre>

  <ul>
    <li><strong>Videos/</strong> – Input videos for use with <code>td3.py</code></li>
    <li><strong>output/</strong> – Annotated output images and video exports</li>
    <li><strong>Traffic Trade/</strong> – Contains trained YOLO model and config files</li>
  </ul>

</body>
</html>
