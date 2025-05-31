import numpy as np
import pyautogui
import cv2
from math import hypot

screen_width, screen_height = pyautogui.size()

def find_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    return np.abs(np.degrees(radians))

def find_distance(landmark_list):
    if len(landmark_list) < 2:
        return 0
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])

def move_mouse(index_finger_tip):
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)

def is__left_click(lm): return (find_angle(lm[5], lm[6], lm[8]) > 90 and
                                find_angle(lm[9], lm[10], lm[12]) < 50 and
                                find_angle(lm[13], lm[14], lm[16]) < 50 and
                                find_angle(lm[17], lm[18], lm[20]) < 50 and
                                find_distance([lm[4], lm[5]]) < 50)

def is__right_click(lm): return (find_angle(lm[5], lm[6], lm[8]) > 90 and
                                 find_angle(lm[9], lm[10], lm[12]) > 90 and
                                 find_angle(lm[13], lm[14], lm[15]) < 50 and
                                 find_angle(lm[17], lm[18], lm[19]) < 50 and
                                 find_distance([lm[4], lm[5]]) < 50)

def is__double_click(lm): return all(find_angle(lm[i], lm[i + 1], lm[i + 2]) < 30 for i in [5, 9, 13, 17]) and \
                                 find_distance([lm[4], lm[5]]) < 50

def is__screenshot(lm): return all(find_angle(lm[i], lm[i + 1], lm[i + 2]) > 90 for i in [5, 9, 13, 17]) and \
                              find_distance([lm[4], lm[5]]) < 20

def all_fingers_up(landmarks):
    return all(landmarks[i][1] < landmarks[i - 2][1] for i in [8, 12, 16, 20])

def get_distance_and_draw(frame, points):
    (x1, y1), (x2, y2) = points
    cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
    cv2.circle(frame, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    return hypot(x2 - x1, y2 - y1)
