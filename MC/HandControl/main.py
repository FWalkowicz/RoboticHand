import time
import cv2
import math
from DetectHand import HandDetector
from DetectGesture import HandGesture
import numpy as np
import cvzone
import os

if __name__ == "__main__":
    end_time = 0
    arm_range = 0
    arm_range_per = 0
    classes = ['MoveX', 'MoveY', 'MoveGrip']
    hand = HandDetector(False, 0.5, 0.5)
    gesture = HandGesture()
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        hand.find_hands(image=frame)
        img = gesture.collect_data(frame.copy())
        # prediction, index = gesture.predict_gesture_tensorflow(frame.copy())
        results = gesture.predict_gesture_tensorflow_lite(frame.copy())
        index = results['id']
        left_landmarks, right_landmarks = hand.find_landmark_position(frame, 0)
        cv2.putText(frame, f"Detection: {classes[index]}", (20, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
        if len(left_landmarks) != 0:
            cv2.circle(frame, (left_landmarks[8][1], left_landmarks[8][2]), 5, (255, 0, 0), cv2.FILLED)

        if len(right_landmarks) != 0:
            cv2.circle(frame, (right_landmarks[4][1], right_landmarks[4][2]), 5, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (right_landmarks[8][1], right_landmarks[8][2]), 5, (0, 255, 255), cv2.FILLED)
            if classes[index] == classes[0]:
                cv2.putText(frame, str(f'x: {right_landmarks[8][1]}'), (20, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            cv2.circle(frame, (right_landmarks[12][1], right_landmarks[12][2]), 5, (0, 255, 255), cv2.FILLED)
            if classes[index] == classes[1]:
                cv2.putText(frame, str(f'y: {right_landmarks[8][2]}'), (20, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            distance = math.hypot(right_landmarks[8][1] - right_landmarks[4][1], right_landmarks[8][2] - right_landmarks[4][2])
            if classes[index] == classes[2]:
                cv2.line(frame, (right_landmarks[4][1], right_landmarks[4][2]),(right_landmarks[8][1], right_landmarks[8][2]), (255, 0, 128), 3)
                cv2.putText(frame, f"Distance: {int(distance)}", (20, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            finger_counter = gesture.finger_counter(right_landmarks)
            cv2.putText(frame, f"Fingers: {finger_counter}", (140, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

            # range 0 - 100
            arm_range = np.interp(distance, [20, 200], [400, 180])
            arm_range_per = (arm_range - 180) / (400 - 180) * 100

        if classes[index] == classes[2]:
            cv2.rectangle(frame, (50, 180), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(frame, (50, 180), (85, int(arm_range)), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f"{int(arm_range_per)}  %", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

        start_time = time.time()
        fps = 1 / (start_time - end_time)
        end_time = start_time
        cv2.putText(frame, f"fps: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        # Create a list of all processed images
        imgList = [frame, img]
        stackedImg = cvzone.stackImages(imgList, 2, 1)

        cv2.imshow('frame', stackedImg)
        if cv2.waitKey(1) == ord('q'):
            break

        """
        if cv2.waitKey(1) == ord('x'):
            cv2.imwrite(f"HandGesture/HandX/hand_{time.time()}.jpg", img)
        if cv2.waitKey(1) == ord('y'):
            cv2.imwrite(f"HandGesture/HandY/hand{time.time()}.jpg", img)
        if cv2.waitKey(1) == ord('g'):
            cv2.imwrite(f"HandGesture/HandGrip/hand{time.time()}.jpg", img)
        """
