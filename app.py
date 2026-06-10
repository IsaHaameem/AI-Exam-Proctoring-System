import streamlit as st
import cv2
import os
import pandas as pd
import time
from datetime import datetime

# Import custom processing modules
from cv.face_detection import FaceDetector
from cv.person_detection import PersonDetector
from cv.phone_detection import PhoneDetector
from cv.gaze_tracking import GazeTracker
from cv.violation_detector import ViolationOrchestrator
from utils.helpers import log_violation

# 1. Page Configuration & Professional White Theme Styling
st.set_page_config(
    page_title="AI Online Exam Proctoring System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean UI injection
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E9ECEF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stActionButton button { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Paths
CSV_PATH = os.path.join("data", "violations.csv")

# 3. Initialize Persistent Session State for Total Violations Count
if "total_violations" not in st.session_state:
    # Read existing row count from CSV to persist counts across web refreshes
    if os.path.exists(CSV_PATH):
        try:
            df_init = pd.read_csv(CSV_PATH)
            st.session_state.total_violations = len(df_init)
        except:
            st.session_state.total_violations = 0
    else:
        st.session_state.total_violations = 0

# UI Layout Header
st.title("🛡️ AI-Based Online Examination Monitoring System")
st.markdown("##### Core Computer Vision Concepts • Final Integrated Architecture")
st.markdown("---")

# Split Dashboard Layout: Left = Camera Processing | Right = Real-time Metrics Matrix
col_feed, col_metrics = st.columns([2, 1])

with col_feed:
    st.markdown("### 📹 Video Proctoring Feed")
    frame_placeholder = st.image([], channels="RGB", width="stretch")
    
    st.markdown("### 🎛️ System Controls")
    run_system = st.checkbox("Activate AI Proctoring Guard", value=False)

with col_metrics:
    st.markdown("### 📊 Status Dashboard")
    
    # Create static layout anchors for metrics to prevent page stuttering
    placeholder_face = st.empty()
    placeholder_people = st.empty()
    placeholder_phone = st.empty()
    placeholder_gaze = st.empty()
    
    st.markdown("---")
    st.markdown("### ⚠️ Session Telemetry")
    placeholder_counter = st.empty()

# Sidebar Log Display Setup
st.sidebar.markdown("## 📜 Violation Event Log")
st.sidebar.markdown("---")
sidebar_log_placeholder = st.sidebar.empty()

def refresh_sidebar_log():
    """Helper to update the sidebar file view without causing full page script refreshes."""
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            if not df.empty:
                sidebar_log_placeholder.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
            else:
                sidebar_log_placeholder.info("Log file clear. No violations recorded yet.")
        except:
            pass

# Initial log load
refresh_sidebar_log()

# 4. Main Computer Vision Execution Pipeline Loop
if run_system:
    # Initialize Core Engines
    with st.spinner("Initializing CV Subsystems..."):
        face_engine = FaceDetector()
        person_engine = PersonDetector()
        phone_engine = PhoneDetector()
        gaze_engine = GazeTracker()
        orchestrator = ViolationOrchestrator()
    
    # Open local hardware video stream capture device (0 = default integrated webcam)
    cap = cv2.VideoCapture(0)
    
    # Set custom frame dimensions for system optimization
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        st.error("Error: Local webcam device hardware connection could not be established.")
        run_system = False

    # Frame Streaming Iteration
    # Frame Streaming Iteration
   # Set up variables for Frame Skipping Optimization
    frame_counter = 0
    PROCESS_EVERY_N_FRAMES = 5  # Run heavy YOLO models only every 5 frames
    
    # Cache variables to hold YOLO data between frames
    cached_person_count = 0
    cached_person_boxes = []
    cached_phone_detected = False
    cached_phone_boxes = []

    # Frame Streaming Iteration
    while run_system and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Dropped frame stream packet. Exiting video loop.")
            break
            
        frame_counter += 1
        annotated_frame = frame.copy()
        
        # --- 1. FAST PROCESSING (Every Frame) ---
        is_face_present, face_detections = face_engine.detect_face(frame)
        gaze_direction = gaze_engine.get_gaze_direction(frame) if is_face_present else "Unknown"
        
        # --- 2. HEAVY PROCESSING (Frame Skipping) ---
        if frame_counter % PROCESS_EVERY_N_FRAMES == 0:
            cached_person_count, cached_person_boxes = person_engine.detect_people(frame)
            cached_phone_detected, cached_phone_boxes = phone_engine.detect_phone(frame)
        
        # --- EXECUTE ORCHESTRATION BEHAVIOR RULES ---
        violation_triggered_face, elapsed_time = orchestrator.check_face_missing(is_face_present)
        if violation_triggered_face:
            if log_violation("Face Missing"):
                st.session_state.total_violations += 1
                refresh_sidebar_log()
                
        violation_triggered_gaze, direction_type = orchestrator.check_gaze(gaze_direction)
        if violation_triggered_gaze:
            if log_violation(f"Looking Away ({direction_type})"):
                st.session_state.total_violations += 1
                refresh_sidebar_log()

        if orchestrator.check_multiple_persons(cached_person_count):
            if log_violation("Multiple Persons Detected"):
                st.session_state.total_violations += 1
                refresh_sidebar_log()
                
        if orchestrator.check_mobile_phone(cached_phone_detected):
            if log_violation("Mobile Phone Detected"):
                st.session_state.total_violations += 1
                refresh_sidebar_log()

        # --- CANVAS ANNOTATION DRAWING LAYER ---
        for (x1, y1, x2, y2) in cached_person_boxes:
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 165, 0), 2)
            cv2.putText(annotated_frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)
            
        for (x1, y1, x2, y2) in cached_phone_boxes:
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(annotated_frame, "WARNING: Mobile Phone", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        gaze_color = (0, 255, 0) if gaze_direction == "Center" else (0, 165, 255)
        cv2.putText(annotated_frame, f"Gaze: {gaze_direction}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, gaze_color, 2)
        
        if not is_face_present and orchestrator.face_missing_start_time is not None:
            missing_sec = round(time.time() - orchestrator.face_missing_start_time, 1)
            cv2.putText(annotated_frame, f"FACE MISSING: {missing_sec}s", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # --- CONVERT & FLUSH TO FRONTEND ---
        rgb_render = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Updated to use width="stretch" to fix Streamlit deprecation warnings
        frame_placeholder.image(rgb_render, channels="RGB", width="stretch")
        
        placeholder_face.metric(label="Face Status", value="✔️ Present" if is_face_present else "❌ Missing")
        placeholder_people.metric(label="Person Count", value=str(cached_person_count), delta=None if cached_person_count <= 1 else "Unauthorized Person")
        placeholder_phone.metric(label="Phone Status", value="🚨 Device Detected!" if cached_phone_detected else "✅ Clear")
        placeholder_gaze.metric(label="Current Gaze Direction", value=gaze_direction)
        placeholder_counter.metric(label="Violations Logged", value=st.session_state.total_violations)
        
    cap.release()
    st.info("AI Monitor Engine Standby Mode Deactivated.")