import cv2
import mediapipe as mp

class GazeTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_gaze_direction(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return "Unknown"

        landmarks = results.multi_face_landmarks[0].landmark
        
        nose_x = landmarks[1].x
        nose_y = landmarks[1].y
        left_x = landmarks[234].x
        right_x = landmarks[454].x
        top_y = landmarks[10].y
        bottom_y = landmarks[152].y
        
        width = right_x - left_x
        height = bottom_y - top_y
        
        if width == 0 or height == 0:
            return "Center"
            
        horiz_ratio = (nose_x - left_x) / width
        vert_ratio = (nose_y - top_y) / height
        
        if horiz_ratio < 0.35:
            return "Right"
        elif horiz_ratio > 0.65:
            return "Left"
        elif vert_ratio > 0.65:
            return "Down"
        else:
            return "Center"