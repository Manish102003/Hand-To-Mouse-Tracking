import cv2
import mediapipe as mp
import random 
import pyautogui
import numpy as np
from pynput.mouse import Button,Controller

mouse=Controller()
mpHands = mp.solutions.hands
hands=mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

pyautogui.FAILSAFE=False
screen_width,screen_height = pyautogui.size()

def find_angle(a,b,c):
    radians = np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def find_distance(landmark_list):
    if(len(landmark_list))<2:
        return
    (x1,y1),(x2,y2)=landmark_list[0],landmark_list[1]
    L =np.hypot(x2-x1,y2-y1)
    return np.interp(L,[0,1],[0,1000]) 

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x=int(index_finger_tip.x * (screen_width+500))
        y=int(index_finger_tip.y * (screen_height+500))
        pyautogui.moveTo(x,y)

def is__left_click(landmarks_list):
    return (find_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) > 90 and
            find_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12]) < 50 and
            find_angle(landmarks_list[13],landmarks_list[14],landmarks_list[16]) < 50 and
            find_angle(landmarks_list[17],landmarks_list[18],landmarks_list[20]) < 50 and
            find_distance([landmarks_list[4],landmarks_list[5]]) < 50
            )

def is__right_click(landmarks_list):
    return (find_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) > 90 and
            find_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12]) > 90 and
            find_angle(landmarks_list[13],landmarks_list[14],landmarks_list[15]) < 50 and
            find_angle(landmarks_list[17],landmarks_list[18],landmarks_list[19]) < 50 and
            find_distance([landmarks_list[4],landmarks_list[5]]) < 50 
            )

def is__double_click(landmarks_list):
    return (find_angle(landmarks_list[5],landmarks_list[6],landmarks_list[7]) < 30 and
            find_angle(landmarks_list[9],landmarks_list[10],landmarks_list[11]) < 30 and
            find_angle(landmarks_list[13],landmarks_list[14],landmarks_list[15]) < 30 and
            find_angle(landmarks_list[17],landmarks_list[18],landmarks_list[19]) < 30 and
            find_distance([landmarks_list[4],landmarks_list[5]]) < 50
            )

def is__screenshot(landmarks_list):
    return (find_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) > 90 and
            find_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12]) > 90 and
            find_angle(landmarks_list[13],landmarks_list[14],landmarks_list[16]) > 90 and
            find_angle(landmarks_list[17],landmarks_list[18],landmarks_list[20]) > 90 and
            find_distance([landmarks_list[4],landmarks_list[5]]) < 20)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None


def detect_gestures(frame,landmarks_list,processed):
    if len(landmarks_list)>=21:
        index_finger_tip = find_finger_tip(processed)

        thumb_index_dist = find_distance([landmarks_list[4],landmarks_list[8]])
        if thumb_index_dist < 50 and find_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8]) > 180:
            move_mouse(index_finger_tip)

        elif is__left_click(landmarks_list):
            mouse.click(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame,"Left Click",(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),4)

        elif is__right_click(landmarks_list):
            mouse.click(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame,"Right Click",(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),4)

        elif is__double_click(landmarks_list):
            pyautogui.doubleClick()
            cv2.putText(frame,"Double Click",(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),4)

        elif is__screenshot(landmarks_list):
            image = pyautogui.screenshot()
            label=random.randint(1,20)
            image.save(f'myscreenshot_{label}.png')
            cv2.putText(frame,"Screenshot Taken",(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)



def main():
    cap = cv2.VideoCapture(0)
    draw=mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret, frame =cap.read()
            if not ret:
                break
            frame = cv2.flip(frame,1)
            frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list = []

            if processed.multi_hand_landmarks:
                
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame,hand_landmarks,mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x,lm.y))
                
            detect_gestures(frame,landmarks_list,processed)

            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Frame', 800, 450)
            cv2.imshow('Frame',frame)

            if not (cv2.getWindowProperty('Frame',cv2.WND_PROP_VISIBLE)):
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()