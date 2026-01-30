import cv2
import mediapipe as mp
import time
from src.calibrator import Calibrator
from src.jump_counter import JumpCounter
from src.visualizer import Visualizer
from src.logger import Logger

def main():
    # MediaPipe 초기화
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # 비디오 캡처
    cap = cv2.VideoCapture("test.mp4")  # 0으로 변경하면 웹캠
    
    if not cap.isOpened():
        print("비디오를 열 수 없습니다")
        return
    
    # 컴포넌트 초기화
    # 기준선 설정
    calibrator = Calibrator(num_frames=30)
    # 점프 기준, 카운팅
    counter = JumpCounter()
    # 시각화
    visualizer = Visualizer()
    # 기록
    logger = Logger()
    
    #start_time 초기화
    start_time = None

    # 메인 루프
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
            
            # 캘리브레이션 단계
            if not calibrator.is_complete:
                print("11")
                calibrator.add_frame(landmarks)
                progress = calibrator.get_progress()
                visualizer.draw_calibration_status(
                    frame, 
                    progress, 
                    len(calibrator.frames), 
                    calibrator.num_frames
                )
                print("22")

            # 캘리브레이션 완료 후 점프 카운팅 단계
            else:
                print("33")
                # 세션 시작 (첫 점프 전)
                if start_time is None:
                    print("start_time is None 조건문 진입")
                    logger.start_session()
                    start_time = time.time()
                    print("조건문 완료")

                # 점프 감지
                jumped = counter.update(landmarks, calibrator.baseline_threshold_y)
                print("점프 감지 완료")

                # 점프 발생 시 기록
                if jumped:
                    elapsed = time.time() - start_time
                    logger.log_jump(counter.count, elapsed)
                
                # 시각화
                visualizer.draw_threshold_line(frame, calibrator.baseline_threshold_y)
                
                ankle_x, ankle_y = counter.get_ankle_position(landmarks)
                visualizer.draw_ankle_marker(frame, ankle_x, ankle_y)
                
                visualizer.draw_stats(frame, counter.count, counter.stage)
            
            # 포즈 랜드마크 그리기
            visualizer.draw_pose_landmarks(frame, results.pose_landmarks)
        
        # 화면 표시
        cv2.imshow("Jump Rope Counter", frame)
        
        # ESC로 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    # 종료 시
    if start_time is not None:
        duration = time.time() - start_time
        logger.end_session(duration)
        
    # 정리
    cap.release()
    cv2.destroyAllWindows()
    pose.close()
    
    # 최종 결과 출력
    print(f"\n=== 운동 결과 ===")
    print(time.strftime("%Y년 %m월 %d일 %H시 %M분 기록"))
    print(f"총 점프 횟수: {counter.count}")

# 이 파일이 직접 실행될 때만 main()을 실행
if __name__ == "__main__":
    main()