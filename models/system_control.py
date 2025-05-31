import time
import cv2
import numpy as np
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from .utilities import all_fingers_up, get_distance_and_draw

volume_device = AudioUtilities.GetSpeakers()
interface = volume_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol, _ = volume.GetVolumeRange()

gesture_states = {
    'volume_control': False,
    'brightness_control': False
}

toggle_timers = {
    'volume': {'start': None, 'active': False},
    'brightness': {'start': None, 'active': False}
}

TOGGLE_HOLD_DURATION = 3

class SystemControl:
    def handle_controls(self, frame, hand_lm, label):
        height, width, _ = frame.shape
        landmarks = [(int(lm.x * width), int(lm.y * height)) for lm in hand_lm.landmark]

        is_all_up = all_fingers_up(landmarks)
        current_time = time.time()
        key = 'volume' if label == 'Left' else 'brightness'

        if is_all_up:
            if not toggle_timers[key]['active']:
                toggle_timers[key]['start'] = current_time
                toggle_timers[key]['active'] = True
            else:
                elapsed = current_time - toggle_timers[key]['start']
                remaining = TOGGLE_HOLD_DURATION - elapsed
                if remaining > 0:
                    cv2.putText(frame, f"{label} Toggle in {remaining:.1f}s", (50, 400 if label == 'Left' else 450),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                else:
                    gesture_states[f"{key}_control"] = not gesture_states[f"{key}_control"]
                    toggle_timers[key]['start'] = None
                    toggle_timers[key]['active'] = False
        else:
            toggle_timers[key]['start'] = None
            toggle_timers[key]['active'] = False

        if label == "Left" and gesture_states['volume_control']:
            distance = get_distance_and_draw(frame, [landmarks[4], landmarks[8]])
            vol = np.interp(distance, [50, 220], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            cv2.putText(frame, f"Volume: {int(63 + vol)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

        if label == "Right" and gesture_states['brightness_control']:
            distance = get_distance_and_draw(frame, [landmarks[4], landmarks[8]])
            b_level = np.interp(distance, [50, 220], [0, 100])
            sbc.set_brightness(int(b_level))
            cv2.putText(frame, f"Brightness: {int(b_level)}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
