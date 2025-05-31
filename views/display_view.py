import cv2

class DisplayView:
    def __init__(self):
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 800, 500)

    def render(self, frame):
        cv2.imshow('Frame', frame)
