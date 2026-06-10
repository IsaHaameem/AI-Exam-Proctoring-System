import time

class ViolationOrchestrator:
    def __init__(self):
        # Face Missing Tracking
        self.face_missing_start_time = None
        self.face_threshold = 5.0 
        
        # Multiple Person Tracking
        self.last_person_violation_time = 0
        
        # Mobile Phone Tracking
        self.last_phone_violation_time = 0
        
        # Gaze Tracking
        self.gaze_away_start_time = None
        self.gaze_threshold = 3.0 # Must look away continuously for 3 seconds
        
        # Universal cooldown to prevent log spam for instant triggers (2 seconds)
        self.cooldown = 2.0 

    def check_face_missing(self, is_face_present):
        if not is_face_present:
            if self.face_missing_start_time is None:
                self.face_missing_start_time = time.time()
            elapsed = time.time() - self.face_missing_start_time
            if elapsed >= self.face_threshold:
                return True, round(elapsed, 1)
        else:
            self.face_missing_start_time = None
        return False, 0

    def check_multiple_persons(self, person_count):
        if person_count > 1:
            current_time = time.time()
            if current_time - self.last_person_violation_time > self.cooldown:
                self.last_person_violation_time = current_time
                return True
        return False

    def check_mobile_phone(self, phone_detected):
        if phone_detected:
            current_time = time.time()
            if current_time - self.last_phone_violation_time > self.cooldown:
                self.last_phone_violation_time = current_time
                return True
        return False

    def check_gaze(self, gaze_direction):
        """
        Logic: If gaze is Left, Right, or Down continuously for 3 seconds, 
        trigger violation. If Center or Unknown, reset the timer.
        """
        if gaze_direction in ["Left", "Right", "Down"]:
            if self.gaze_away_start_time is None:
                self.gaze_away_start_time = time.time()
            elapsed = time.time() - self.gaze_away_start_time
            
            if elapsed >= self.gaze_threshold:
                # Trigger violation and reset timer so it triggers again if they keep looking away
                self.gaze_away_start_time = time.time() 
                return True, gaze_direction
        else:
            # Student looked back at the center
            self.gaze_away_start_time = None
            
        return False, None