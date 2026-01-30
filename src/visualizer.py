import cv2
import mediapipe as mp

class Visualizer:
    """화면 시각화 담당 클래스"""
    
    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
    
    def draw_calibration_status(self, frame, progress, current, total):
        """캘리브레이션 진행 상황 표시"""
        cv2.putText(frame, "Stand still for calibration...", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2)
        cv2.putText(frame, f"{current}/{total}", 
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2)
    
    def draw_threshold_line(self, frame, baseline_threshold_y):
        """기준선 그리기"""
        h, w = frame.shape[:2]
        line_y = int(baseline_threshold_y * h)
        
        cv2.line(frame, (0, line_y), (w, line_y), (0, 0, 255), 3)
        cv2.putText(frame, "Jump Threshold", 
                    (w - 200, line_y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    def draw_ankle_marker(self, frame, ankle_x, ankle_y):
        """발목 위치 표시"""
        h, w = frame.shape[:2]
        screen_x = int(ankle_x * w)
        screen_y = int(ankle_y * h)
        cv2.circle(frame, (screen_x, screen_y), 10, (0, 255, 0), -1)
    
    def draw_stats(self, frame, count, stage):
        """통계 정보 표시"""
        cv2.putText(frame, f'Count: {count}', 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.5, (0, 255, 0), 3)
        cv2.putText(frame, f'Stage: {stage if stage else "ready"}', 
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2)
    
    def draw_pose_landmarks(self, frame, pose_landmarks):
        """포즈 랜드마크 그리기"""
        self.mp_draw.draw_landmarks(
            frame,
            pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS
        )