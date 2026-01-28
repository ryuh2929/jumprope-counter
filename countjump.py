import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()
cap = cv2.VideoCapture("test.mp4")

# 카운팅 변수
count = 0
stage = None  # "up" 또는 "down"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # 발목 y좌표 (0~1 정규화)
        left_ankle = landmarks[27].y
        right_ankle = landmarks[28].y
        avg_ankle = (left_ankle + right_ankle) / 2
        
        # 임계값 (화면 하단 기준, 조정 필요)
        threshold = 0.8
        
        # 상태 변화 감지
        if avg_ankle < threshold:  # 발이 올라감
            stage = "up"
        if avg_ankle > threshold and stage == "up":  # 발이 내려감
            stage = "down"
            count += 1
        
        # 화면에 표시
        cv2.putText(frame, f'Count: {count}', 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
        
        mp_draw.draw_landmarks(frame, results.pose_landmarks, 
                               mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Jump Rope Counter", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


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