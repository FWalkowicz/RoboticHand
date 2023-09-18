import os.path
import cv2
import math
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import tensorflow as tf


class HandGesture:
    def __init__(self):
        self.image_dir = os.path.join(os.getcwd(), 'HandGesture')
        self.detector = HandDetector(maxHands=2)
        self.classifier = Classifier('/home/filip/PycharmProjects/Comcore_Sensors/MC/HandControl/Models/keras_model.h5', '/home/filip/PycharmProjects/Comcore_Sensors/MC/HandControl/Models/labels.txt')
        self.interpreter = tf.lite.Interpreter(model_path='/home/filip/PycharmProjects/Comcore_Sensors/MC/HandControl/Models/model_unquant.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def collect_data(self, image):
        hands, img = self.detector.findHands(image)
        img_white = np.ones((224, 224, 3), np.uint8)
        img_white = cv2.bitwise_not(img_white)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            crop_image = img[y - 20: y + h + 20, x - 20: x + w + 20]
            aspect_ratio = h/w
            if aspect_ratio > 1:
                k = 224 / h
                w_cal = math.ceil(k * w)
                img_resize = cv2.resize(crop_image, (w_cal, 224))
                # Resize img_resize to match the shape of img_white
                img_resize = cv2.resize(img_resize, (img_white.shape[1], img_white.shape[0]))
                img_white[0:img_resize.shape[0], 0:img_resize.shape[1]] = img_resize

        return img_white

    def predict_gesture_tensorflow(self, image):
        image_prediction = self.collect_data(image)
        prediction, index = self.classifier.getPrediction(image_prediction)

        return prediction, index

    def predict_gesture_tensorflow_lite(self, image):
        image_prediction = self.collect_data(image)
        image_prediction = cv2.cvtColor(image_prediction, cv2.COLOR_BGR2GRAY)
        input_data = cv2.resize(image_prediction, (224, 224))
        input_data_rgb = cv2.cvtColor(input_data, cv2.COLOR_GRAY2RGB)
        input_data_rgb = input_data_rgb.astype(np.float32) / 255.0
        input_data_rgb = np.expand_dims(input_data_rgb, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data_rgb)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        class_predictions = np.argmax(output_data)
        class_labels = [2, 1, 0]

        # Get the predicted class label
        predicted_class = class_labels[class_predictions]

        results = {'id': predicted_class}
        return results

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

