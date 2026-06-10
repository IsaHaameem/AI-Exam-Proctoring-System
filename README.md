# 🎓 AI-Based Online Examination Monitoring System

A lightweight Computer Vision-based online examination monitoring system developed as a Computer Vision course project. The system uses real-time webcam input to monitor candidate behavior and detect suspicious activities such as looking away from the screen, absence from the camera, presence of multiple people, and mobile phone usage.

The project is implemented using **Python**, **OpenCV**, **MediaPipe**, **YOLOv8**, and **Streamlit**.

---

# 📌 Project Overview

Online examinations have become increasingly common in educational institutions. Ensuring academic integrity during remote assessments remains a significant challenge.

This project provides a simple AI-powered proctoring solution that monitors students through a webcam and automatically identifies potential examination violations using Computer Vision techniques.

---

# 🎯 Objectives

* Detect whether the student is present in front of the camera.
* Monitor head orientation and gaze direction.
* Detect multiple people in the examination environment.
* Detect mobile phones or other unauthorized devices.
* Maintain a log of suspicious activities.
* Provide a simple and interactive monitoring dashboard.

---

# 🏗️ System Architecture

```text
Webcam Feed
      │
      ▼
Frame Acquisition
      │
      ▼
Computer Vision Pipeline
      │
 ┌────┼─────────────────────┐
 ▼    ▼                     ▼
Face Detection       Gaze Tracking
(MediaPipe)          (Face Mesh)

 ▼
YOLOv8 Object Detection
(Person & Mobile Phone)

      │
      ▼
Violation Detection Engine
      │
      ▼
Dashboard + CSV Logging
```

---

# 📂 Project Structure

```text
exam_proctor_project/
│
├── app.py
│
├── cv/
│   ├── face_detection.py
│   ├── gaze_tracking.py
│   ├── person_detection.py
│   └── violation_detector.py
│
├── utils/
│   └── helpers.py
│
├── data/
│   └── violations.csv
│
├── models/
│   └── yolov8n.pt
│
└── .streamlit/
    └── config.toml
```

---

# ✨ Features

## 1. Face Presence Detection

The system continuously checks whether a face is visible in the webcam feed.

**Violation Trigger:**

* No face detected for more than 5 seconds.

---

## 2. Gaze Monitoring

MediaPipe Face Mesh is used to track facial landmarks and estimate head orientation.

**Violation Trigger:**

* Looking away from the screen continuously for more than 3 seconds.

Detected directions include:

* Looking Left
* Looking Right
* Looking Down

---

## 3. Multiple Person Detection

YOLOv8 detects the number of people visible in the frame.

**Violation Trigger:**

* More than one person detected.

---

## 4. Mobile Phone Detection

YOLOv8 identifies mobile phones using the COCO dataset classes.

**Violation Trigger:**

* Mobile phone detected in the examination area.

---

## 5. Violation Logging

All detected violations are automatically recorded with timestamps in:

```text
data/violations.csv
```

Sample Log:

```csv
Timestamp,Violation
2026-06-10 10:12:45,Looking Away
2026-06-10 10:15:03,Mobile Phone Detected
2026-06-10 10:18:20,Multiple Persons Detected
```

---

# ⚡ Performance Optimization

To improve performance on systems without dedicated GPUs:

* Face detection runs on every frame.
* YOLOv8 inference runs every 5th frame.
* Detection results are temporarily cached.
* Reduces CPU workload while maintaining monitoring accuracy.

---

# 🛠️ Technologies Used

| Technology | Purpose                    |
| ---------- | -------------------------- |
| Python     | Core Programming Language  |
| OpenCV     | Image Processing           |
| MediaPipe  | Face Detection & Face Mesh |
| YOLOv8     | Person & Phone Detection   |
| Streamlit  | Web Dashboard              |
| Pandas     | Data Logging               |
| CSV        | Violation Storage          |

---

# 💻 Installation

## Prerequisites

* Python 3.11+
* VS Code (Recommended)
* Windows/Linux/macOS

---

## Clone Repository

```bash
git clone <repository-url>
cd exam_proctor_project
```

---

## Create Virtual Environment

### Windows

```powershell
py -3.11 -m venv venv

.\venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install streamlit
pip install opencv-python
pip install mediapipe==0.10.9
pip install ultralytics
pip install pandas
```

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Enable monitoring using the dashboard controls and allow webcam access when prompted.

---

# 📊 Expected Output

The dashboard displays:

* Live Webcam Feed
* Face Detection Status
* Gaze Direction
* Person Count
* Mobile Phone Detection Status
* Violation Alerts
* Violation History Log

---

# 🔮 Future Improvements

* Face Recognition for candidate verification
* Browser activity monitoring
* Audio anomaly detection
* Examination session recording
* Cloud-based violation storage
* Administrator monitoring dashboard

---

# 📚 Academic Relevance

This project demonstrates practical applications of:

* Computer Vision
* Object Detection
* Face Landmark Detection
* Human Behavior Analysis
* Real-Time Monitoring Systems

and serves as a mini-project for Computer Vision coursework.

---

# 👨‍💻 Authors

**Muhammad Isa Haameem**


This project is developed solely for academic and educational purposes.
