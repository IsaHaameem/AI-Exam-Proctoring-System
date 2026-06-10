from ultralytics import YOLO
import cv2
import os

class PhoneDetector:
    def __init__(self):
        # We reuse the lightweight YOLOv8 Nano model. 
        # Since it's already downloaded from Phase 7, it will load instantly.
        self.model = YOLO("yolov8n.pt")
        
    def detect_phone(self, frame):
        """
        Detects mobile phones in the frame and returns a boolean flag and bounding boxes.
        COCO Class ID for 'cell phone' is 67.
        """
        # Run inference on the current frame
        results = self.model(frame, verbose=False, stream=False)
        
        phone_detected = False
        boxes = []
        
        # Parse the results
        for r in results:
            for box in r.boxes:
                # Class 67 is 'cell phone' in the COCO dataset
                if int(box.cls) == 67:
                    phone_detected = True
                    # Extract coordinates to draw a warning box in the UI later
                    x1, y1, x2, y2 = box.xyxy[0]
                    boxes.append((int(x1), int(y1), int(x2), int(y2)))
        
        return phone_detected, boxes