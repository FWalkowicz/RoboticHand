import os.path

import cv2
import mediapipe as mp


class HandGesture:
    def __init__(self):
        self.image_dir = os.path.join(os.getcwd(), 'HandGesture')

    def image_processing(self):
        image_list = os.listdir(self.image_dir)

    @staticmethod
    def finger_counter(lm_list):
        finger_tip_id = [4, 8, 12, 16, 20]
        gesture_list = []

        if lm_list[finger_tip_id[0]][1] > lm_list[finger_tip_id[0] - 1][1]:
            gesture_list.append(1)
        else:
            gesture_list.append(0)

        for id_lm in range(1, 5):
            if lm_list[finger_tip_id[id_lm]][2] < lm_list[finger_tip_id[id_lm] - 2][2]:
                gesture_list.append(1)
            else:
                gesture_list.append(0)

        return gesture_list


if __name__ == "__main__":
    pass
