from ultralytics import YOLO
import cv2
import os

class PersonDetector:
    def __init__(self):
        # Load the pre-trained YOLOv8 Nano model (Lightweight for real-time)
        # It will automatically download 'yolov8n.pt' on first run
        model_path = os.path.join("models", "yolov8n.pt")
        self.model = YOLO("yolov8n.pt") # Loads to root, then we can move it
        
    def detect_people(self, frame):
        """
        Detects persons in the frame and returns the count and annotated boxes.
        COCO Class ID for Person is 0.
        """
        results = self.model(frame, verbose=False, stream=False)
        
        person_count = 0
        boxes = []
        
        # results[0] contains the detection for the current frame
        for r in results:
            for box in r.boxes:
                # Class 0 is 'person' in the COCO dataset
                if int(box.cls) == 0:
                    person_count += 1
                    # Extract coordinates for drawing in UI
                    x1, y1, x2, y2 = box.xyxy[0]
                    boxes.append((int(x1), int(y1), int(x2), int(y2)))
        
        return person_count, boxes