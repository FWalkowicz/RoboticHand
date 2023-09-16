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
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        # draw hand landmarks
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)

        return image

    def find_landmark_position(self, image, landmark_number):
        """

        @param image:
        @param landmark_number:
        @return:
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            searching_hand = self.results.multi_hand_landmarks[landmark_number]
            for id_lms, lm in enumerate(searching_hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id_lms, cx, cy])
        return lm_list


if __name__ == "__main__":
    hand = HandDetector(False, 0.5, 0.5)
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        hand.find_hands(image=frame)
        four_right = hand.find_landmark_position(frame, 0)
        if len(four_right) != 0:
            cv2.circle(frame, (four_right[4][1], four_right[4][2]), 5, (255, 0, 0), cv2.FILLED)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
