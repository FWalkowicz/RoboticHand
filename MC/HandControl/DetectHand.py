"""

"""
import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode: bool, max_conf: float, min_conf: float):
        """

        @param mode:
        @param max_conf:
        @param min_conf:
        """
        if not (0 <= max_conf <= 1):
            raise ValueError("max_conf must be in the range [0, 1]")
        if not (0 <= min_conf <= 1):
            raise ValueError("min_conf must be in the range [0, 1]")
        self.mode = mode
        self.num_hands = 2
        self.max_detection_confidence = max_conf
        self.min_tracking_confidence = min_conf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.num_hands,
            min_detection_confidence=self.max_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, image):
        """

        @param image:
        @return:
        """
        img_flip = cv2.flip(image, 1)
        img_rgb = cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        return image

    def find_landmark_position(self, image, landmark_number):
        """

        @param image:
        @param landmark_number:
        @return:
        """
        left_hand_landmarks = []
        right_hand_landmarks = []
        if self.results.multi_hand_landmarks:
            for landmark_number, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                hand_label = self.results.multi_handedness[landmark_number].classification[0].label
                for id_lms, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cx_flipped = w - cx
                    cy_flipped = cy
                    landmark_info = [id_lms, cx_flipped, cy_flipped]

                    if hand_label == 'Left':
                        left_hand_landmarks.append(landmark_info)
                    elif hand_label == 'Right':
                        right_hand_landmarks.append(landmark_info)
        return left_hand_landmarks, right_hand_landmarks


