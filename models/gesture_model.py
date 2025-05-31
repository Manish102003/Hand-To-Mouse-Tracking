import pyautogui
import random
from pynput.mouse import Button, Controller
from .utilities import *

mouse = Controller()

gesture_states = {
    'left_click': False,
    'right_click': False,
    'double_click': False,
    'screenshot': False
}

class GestureModel:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def handle_gestures(self, landmarks, processed, frame):
        if len(landmarks) >= 21:
            index_tip = processed.multi_hand_landmarks[0].landmark[8]
            move_mouse(index_tip)

            if is__left_click(landmarks):
                if not gesture_states['left_click']:
                    mouse.click(Button.left)
                    gesture_states['left_click'] = True
                    cv2.putText(frame, "Left Click", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4)
            else:
                gesture_states['left_click'] = False

            if is__right_click(landmarks):
                if not gesture_states['right_click']:
                    mouse.click(Button.right)
                    gesture_states['right_click'] = True
                    cv2.putText(frame, "Right Click", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
            else:
                gesture_states['right_click'] = False

            if is__double_click(landmarks):
                if not gesture_states['double_click']:
                    pyautogui.doubleClick()
                    gesture_states['double_click'] = True
                    cv2.putText(frame, "Double Click", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            else:
                gesture_states['double_click'] = False

            if is__screenshot(landmarks):
                if not gesture_states['screenshot']:
                    label = random.randint(1, 100)
                    pyautogui.screenshot(f"myscreenshot_{label}.png")
                    gesture_states['screenshot'] = True
                    cv2.putText(frame, "Screenshot Taken", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            else:
                gesture_states['screenshot'] = False
