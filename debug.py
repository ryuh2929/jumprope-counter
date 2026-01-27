import traceback
print("디벅")
try:
    print("try")
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
except Exception:
    print("error")
    traceback.print_exc()
