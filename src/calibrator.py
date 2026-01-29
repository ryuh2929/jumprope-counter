class Calibrator:
    
    # 기준선 캘리브레이션
    def __init__(self, num_frames=30):
        self.num_frames = num_frames # 1초 (30fps 기준)
        self.frames = []
        self.baseline_threshold_y = None # 기준선 절대 위치
        self.is_complete = False
    
    def add_frame(self, landmarks):

        if self.is_complete:
            return
        
        hip_y = (landmarks[23].y + landmarks[24].y) / 2
        ankle_y = (landmarks[27].y + landmarks[28].y) / 2