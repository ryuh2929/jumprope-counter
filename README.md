# jumprope-counter

<img width="961" height="481" alt="JumpRope Counter" src="https://github.com/user-attachments/assets/61ac5097-0631-4afd-ad5b-c373dd2512ab" />

# MediaPipe Pose Test

간단한 MediaPipe 포즈 감지 및 관절 그리기 데모입니다.

# 버전 정보
`Python 3.9.13`
`mediapipe 0.10.9`
`opencv-python 4.13.0.90`

## 요구사항 설치:

```bash
pip install -r requirements.txt
```

# 실행
```bash
python3 countjump.py
```

# 주요 구현 기록
- MediaPipe 버전 호환성 문제로 Python 최신 버전에서 실행 불가, Python 구버전 설치 (최신 버전과 호환되는 MediaPipe Tasks는 API가 복잡하고 무거워서 간단한 동작에는 구버전 MediaPipe가 선호됨)
- 골반-발목 길이 비례해서 기준선 선정
- 확장성을 위해 Pandas DataFrame 기반 점프 시각, 횟수, RPM 등 운동 데이터 기록 및 세션별 통계 CSV 저장
