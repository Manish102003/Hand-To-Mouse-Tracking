Gesture Control System
A real-time hand gesture recognition system that enables mouse control, volume adjustment, brightness control, and screenshot capture using hand gestures detected via a webcam. Built with MediaPipe, OpenCV, PyAutoGUI, and system-level APIs.
Features

* **Mouse Movement:** Move the mouse cursor by moving your index finger.
* **Left Click:** Perform a left mouse click using a specific hand gesture.
* **Right Click:** Perform a right mouse click with a different gesture.
* **Double Click:** Perform a double click using another gesture.
* **Screenshot Capture:** Take screenshots with a dedicated hand gesture.
* **Volume Control:** Toggle and adjust system volume by holding a gesture on the left hand.
* **Brightness Control:** Toggle and adjust screen brightness by holding a gesture on the right hand.
* **Hold-to-Toggle Control Modes:** Volume and brightness controls are activated only after holding the toggle gesture for 3 seconds, preventing accidental switches.
* **Visual Feedback:** On-screen text displays current actions and countdown timers for toggling controls.

## Installation

### Requirements

* Python 3.7+
* Windows OS (for volume and brightness control)
* Webcam

### Python Packages

Install required Python packages via pip:

```bash
pip install opencv-python mediapipe numpy pyautogui screen_brightness_control pynput pycaw comtypes
```

---

## Usage

Run the main script:

```bash
python main.py
```

### Controls

| Gesture                                     | Action                                         |
| ------------------------------------------- | ---------------------------------------------- |
| Move index finger                           | Move mouse cursor                              |
| Left click gesture                          | Perform left mouse click                       |
| Right click gesture                         | Perform right mouse click                      |
| Double click gesture                        | Perform double mouse click                     |
| Screenshot gesture                          | Take a screenshot                              |
| Hold all fingers up (Left hand)             | Toggle volume control mode after 3 seconds     |
| Hold all fingers up (Right hand)            | Toggle brightness control mode after 3 seconds |
| Volume control mode active (Left hand)      | Adjust volume by pinching distance             |
| Brightness control mode active (Right hand) | Adjust brightness by pinching distance         |

Press **`q`** to quit the program.

## Folder Structure (MVC)

* **model/** - Contains logic related to gesture detection, audio and brightness control.
* **view/** - Contains UI related code (displaying camera feed and text overlays).
* **controller/** - Handles input processing and interaction between model and view.

## Notes

* Ensure your webcam is enabled and accessible.
* Volume and brightness control use Windows-specific APIs (`pycaw` and `screen_brightness_control`).
* Gestures may vary slightly based on lighting and webcam quality.
* You may need to adjust gesture thresholds for better accuracy depending on your environment.

## Troubleshooting

* If volume or brightness controls do not work, verify your OS and permissions.
* For brightness adjustment, the system must support software control of the backlight.
* If the webcam feed does not appear, check your webcam connection and permissions.
