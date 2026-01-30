class JumpCounter:
    """점프 카운팅 담당 클래스"""
    
    def __init__(self):
        self.count = 0
        self.stage = None
    
    def update(self, landmarks, baseline_threshold_y):
        """
        점프 감지 및 카운트 업데이트
        
        Returns:
            bool: 이번 프레임에서 점프가 감지되었는지
        """
        ankle_y = self._get_ankle_y(landmarks)
        jumped = False
        
        # 발목이 기준선 위로
        if ankle_y < baseline_threshold_y:
            self.stage = "up"
        
        # 발목이 기준선 아래로 (점프 완료)
        if ankle_y > baseline_threshold_y and self.stage == "up":
            self.count += 1
            self.stage = "down"
            jumped = True
        
        return jumped
    
    def _get_ankle_y(self, landmarks):
        """발목 평균 y좌표 계산"""
        left_ankle_y = landmarks[27].y
        right_ankle_y = landmarks[28].y
        return (left_ankle_y + right_ankle_y) / 2
    
    def get_ankle_position(self, landmarks):
        """발목 화면 좌표 반환 (x, y)"""
        ankle_x = (landmarks[27].x + landmarks[28].x) / 2
        ankle_y = self._get_ankle_y(landmarks)
        return ankle_x, ankle_y