import time
import cv2
import math
from DetectHand import HandDetector
import numpy as np

if __name__ == "__main__":
    end_time = 0
    arm_range = 0
    arm_range_per = 0
    hand = HandDetector(False, 0.5, 0.5)
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        hand.find_hands(image=frame)
        left_landmarks, right_landmarks = hand.find_landmark_position(frame, 0)
        if len(left_landmarks) != 0:
            cv2.circle(frame, (left_landmarks[8][2], left_landmarks[8][3]), 5, (255, 0, 0), cv2.FILLED)

        if len(right_landmarks) != 0:
            cv2.circle(frame, (right_landmarks[4][2], right_landmarks[4][3]), 5, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (right_landmarks[8][2], right_landmarks[8][3]), 5, (0, 255, 255), cv2.FILLED)
            cv2.putText(frame, str(f'x: {right_landmarks[8][2]}'), (20, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            cv2.circle(frame, (right_landmarks[12][2], right_landmarks[12][3]), 5, (0, 255, 255), cv2.FILLED)
            cv2.putText(frame, str(f'y: {right_landmarks[8][3]}'), (150, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            cv2.line(frame, (right_landmarks[4][2], right_landmarks[4][3]), (right_landmarks[8][2], right_landmarks[8][3]), (255, 0, 128), 3)
            distance = math.hypot(right_landmarks[8][2] - right_landmarks[4][2], right_landmarks[8][3] - right_landmarks[4][3])
            cv2.putText(frame, f"Distance: {int(distance)}", (280, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

            # range 0 - 100
            arm_range = np.interp(distance, [20, 200], [400, 150])
            arm_range_per = (arm_range - 150) / (400 - 150) * 100

        cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, 150), (85, int(arm_range)), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f"{int(arm_range_per)}  %", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        start_time = time.time()
        fps = 1 / (start_time - end_time)
        end_time = start_time
        cv2.putText(frame, f"fps: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
