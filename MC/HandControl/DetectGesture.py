import os.path

import cv2
import mediapipe as mp


class HandGesture:
    def __init__(self):
        self.image_dir = os.path.join(os.getcwd(), 'hand_gesture')

    def image_processing(self):
        image_list = os.listdir(self.image_dir)

    def finger_counter(self):
        pass


if __name__ == "__main__":
    pass
