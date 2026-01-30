import os
from datetime import datetime
import pandas as pd


class Logger:
    """운동 기록 및 통계 관리 클래스"""
    
    def __init__(self):
        # logs 폴더 생성
        os.makedirs("logs", exist_ok=True)
        
        # 세션 ID
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # DataFrame 초기화
        self.df = pd.DataFrame(columns=[
            'session_id', 'timestamp', 'jump_number', 
            'interval', 'cumulative_time', 'rpm'
        ])
        
        # 세션 정보
        self.start_time = None
        self.duration = 0
    
    def start_session(self):
        """세션 시작"""
        self.start_time = datetime.now()
        print(f"\n운동 시작: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"세션 ID: {self.session_id}")
        print("-" * 50)
    
    def log_jump(self, jump_number, timestamp):
        """
        점프 기록
        
        Args:
            jump_number (int): 점프 번호
            timestamp (float): 누적 시간 (초)
        """
        # 이전 점프와의 간격 계산
        interval = 0.0
        if len(self.df) > 0:
            interval = timestamp - self.df.iloc[-1]['cumulative_time']
        
        # RPM 계산
        rpm = self._calculate_rpm(timestamp)
        
        # DataFrame에 추가
        new_row = pd.DataFrame([{
            'session_id': self.session_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jump_number': jump_number,
            'interval': interval,
            'cumulative_time': timestamp,
            'rpm': rpm
        }])
        
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        
        # 콘솔 출력
        self._print_jump_info(jump_number, timestamp, interval, rpm)
    
    def _calculate_rpm(self, current_time):
        """
        최근 10개 점프 기준 RPM 계산
        
        Args:
            current_time (float): 현재 누적 시간
            
        Returns:
            float: RPM (분당 회수)
        """
        if len(self.df) < 2:
            return 0.0
        
        # 최근 10개 (또는 전체)
        recent = self.df.tail(10)
        time_span = current_time - recent.iloc[0]['cumulative_time']
        
        if time_span == 0:
            return 0.0
        
        # RPM = (점프 수 / 시간) * 60
        jumps_count = len(recent) - 1
        rpm = (jumps_count / time_span) * 60
        
        return rpm
    
    def _print_jump_info(self, jump_number, timestamp, interval, rpm):
        """콘솔에 점프 정보 출력"""
        elapsed = f"{int(timestamp // 60):02d}:{int(timestamp % 60):02d}"
        print(f"[{elapsed}] Jump #{jump_number:3d} | "
              f"Interval: {interval:.2f}s | "
              f"RPM: {rpm:5.1f}")
    
    def get_stats(self):
        """
        운동 통계 계산 (나중에 카톡 메세지에서 재사용 가능)
        
        Returns:
            dict: 운동 통계 정보
        """
        if len(self.df) == 0:
            return None
        
        # 간격 계산 (첫 점프 제외)
        intervals = self.df['interval'].iloc[1:].tolist()
        
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': datetime.now().isoformat(),
            'duration': self.duration,
            'total_jumps': len(self.df),
            'average_rpm': float(self.df['rpm'].mean()) if len(self.df) > 0 else 0,
            'max_rpm': float(self.df['rpm'].max()) if len(self.df) > 0 else 0,
            'min_rpm': float(self.df[self.df['rpm'] > 0]['rpm'].min()) if any(self.df['rpm'] > 0) else 0,
            'average_interval': sum(intervals) / len(intervals) if intervals else 0,
            'max_interval': max(intervals) if intervals else 0,
            'min_interval': min(intervals) if intervals else 0
        }
    
    def save_csv(self):
        """CSV 파일로 저장"""
        csv_file = f"logs/jumps_{self.session_id}.csv"
        self.df.to_csv(csv_file, index=False)
        print(f"CSV 저장: {csv_file}")
    
    def print_summary(self):
        """운동 요약 출력"""
        stats = self.get_stats()
        
        if not stats:
            print("기록된 점프가 없습니다.")
            return
        
        print("\n" + "=" * 50)
        print("운동 종료!")
        print("=" * 50)
        print(f"총 점프 횟수: {stats['total_jumps']}회")
        print(f"운동 시간: {int(stats['duration'] // 60)}분 {int(stats['duration'] % 60)}초")
        print(f"평균 RPM: {stats['average_rpm']:.1f}")
        print(f"최고 RPM: {stats['max_rpm']:.1f}")
        print(f"평균 간격: {stats['average_interval']:.2f}초")
        print("=" * 50)
    
    def end_session(self, duration):
        """
        세션 종료
        
        Args:
            duration (float): 총 운동 시간 (초)
        """
        self.duration = duration
        
        # CSV 저장
        self.save_csv()
        
        # 요약 출력
        self.print_summary()
    
    def get_dataframe(self):
        """
        DataFrame 반환 (추가 분석용)
        
        Returns:
            pd.DataFrame: 점프 기록 데이터
        """
        return self.df.copy()