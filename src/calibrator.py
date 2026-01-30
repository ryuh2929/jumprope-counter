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
        self.frames.append({
            'hip_y': hip_y,
            'ankle_y': ankle_y
        })
        
        if len(self.frames) >= self.num_frames:
            self._calculate_baseline()
    
    def _calculate_baseline(self):
        """기준선 계산"""
        # 평균 엉덩이-발목 거리 계산
        avg_hip_y = sum(f['hip_y'] for f in self.frames) / len(self.frames)
        avg_ankle_y = sum(f['ankle_y'] for f in self.frames) / len(self.frames)
        baseline_distance = avg_ankle_y - avg_hip_y
        
        # 기준선: 엉덩이에서 발목까지 거리의 90% 지점 (10% 올라간 위치)
        self.baseline_threshold_y = avg_hip_y + (baseline_distance * 0.9)
        self.is_complete = True
        
        print(f"Calibration complete!")
        print(f"Baseline threshold Y: {self.baseline_threshold_y:.3f}")
    
    def get_progress(self):
        """진행률 반환 (0.0 ~ 1.0)"""
        return len(self.frames) / self.num_frames