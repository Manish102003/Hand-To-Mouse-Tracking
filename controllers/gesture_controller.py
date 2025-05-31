import cv2
import time
import mediapipe as mp
from models.gesture_model import GestureModel
from models.system_control import SystemControl
from views.display_view import DisplayView

class GestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model = GestureModel()
        self.system_control = SystemControl()
        self.view = DisplayView()
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            max_num_hands=2
        )
        self.draw = mp.solutions.drawing_utils

    def run(self):
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = self.hands.process(frameRGB)

                if result.multi_hand_landmarks:
                    for i, hand_lms in enumerate(result.multi_hand_landmarks):
                        label = "Left" if i == 0 else "Right"
                        self.draw.draw_landmarks(frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

                        landmarks = [(lm.x, lm.y) for lm in hand_lms.landmark]
                        self.model.handle_gestures(landmarks, result, frame)
                        self.system_control.handle_controls(frame, hand_lms, label)

                self.view.render(frame)

                if not cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE):
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
