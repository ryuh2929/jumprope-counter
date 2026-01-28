import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture("test.mp4")

if not cap.isOpened():
    print("카메라를 열 수 없습니다")
    exit()

# 카운팅 변수
count = 0
stage = None

# 기준선 캘리브레이션
baseline_threshold_y = None  # 기준선 절대 위치
calibration_frames = []
calibration_complete = False
CALIBRATION_FRAMES = 30  # 1초 (30fps 기준)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다")
        break

    # MediaPipe 처리
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # 엉덩이 중심
        hip_y = (landmarks[23].y + landmarks[24].y) / 2
        
        # 발목 평균
        left_ankle_y = landmarks[27].y
        right_ankle_y = landmarks[28].y
        avg_ankle_y = (left_ankle_y + right_ankle_y) / 2
        
        # 캘리브레이션 단계
        if not calibration_complete:
            calibration_frames.append({
                'hip_y': hip_y,
                'ankle_y': avg_ankle_y
            })
            
            # 캘리브레이션 진행 상황 표시
            cv2.putText(frame, "Stand still for calibration...", 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 0, 255), 2)
            cv2.putText(frame, f"{len(calibration_frames)}/{CALIBRATION_FRAMES}", 
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 0, 255), 2)
            
            if len(calibration_frames) >= CALIBRATION_FRAMES:
                # 평균 엉덩이-발목 거리 계산
                avg_hip_y = sum(f['hip_y'] for f in calibration_frames) / len(calibration_frames)
                avg_ankle_y = sum(f['ankle_y'] for f in calibration_frames) / len(calibration_frames)
                baseline_distance = avg_ankle_y - avg_hip_y
                
                # 기준선: 엉덩이에서 발목까지 거리의 90% 지점 (10% 올라간 위치)
                baseline_threshold_y = avg_hip_y + (baseline_distance * 0.9)
                
                calibration_complete = True
                print(f"Calibration complete!")
                print(f"Baseline threshold Y: {baseline_threshold_y:.3f}")
        
        # 캘리브레이션 완료 후 점프 카운팅
        else:
            # 발목이 기준선보다 위에 있는지 체크 (y값이 작을수록 위)
            if avg_ankle_y < baseline_threshold_y:  # 발이 기준선 위로 올라감
                stage = "up"
            
            if avg_ankle_y > baseline_threshold_y and stage == "up":  # 발이 기준선 아래로 내려감
                count += 1
                stage = "down"
            
            # 화면 크기
            h, w = frame.shape[:2]
            
            # 고정된 기준선 위치
            line_y = int(baseline_threshold_y * h)
            
            # 기준선 그리기 (빨간색)
            cv2.line(frame, (0, line_y), (w, line_y), (0, 0, 255), 3)
            cv2.putText(frame, "Jump Threshold", 
                        (w - 200, line_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # 현재 발목 위치 표시 (초록색 점)
            ankle_screen_y = int(avg_ankle_y * h)
            ankle_screen_x = int((landmarks[27].x + landmarks[28].x) / 2 * w)
            cv2.circle(frame, (ankle_screen_x, ankle_screen_y), 10, (0, 255, 0), -1)
            
            # 정보 표시
            cv2.putText(frame, f'Count: {count}', 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1.5, (0, 255, 0), 3)
            cv2.putText(frame, f'Stage: {stage if stage else "ready"}', 
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 255, 255), 2)
        
        # 포즈 랜드마크 그리기
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("Jump Rope Counter", frame)

    # ESC로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pose.close()

## 📊 관절 좌표 정보

# MediaPipe Pose는 **33개 관절** 제공:
# - **좌표**: (x, y, z) - 모두 0~1로 정규화
# - **y좌표**: 0 = 화면 상단, 1 = 화면 하단
# - **주요 관절**:
# ```
#   0: 코
#   11-12: 어깨
#   13-14: 팔꿈치
#   15-16: 손목
#   23-24: 엉덩이
#   25-26: 무릎
#   27-28: 발목