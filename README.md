\# Hand Gesture Recognition and Computer Control



A real-time hand gesture recognition system built using Python, OpenCV, and MediaPipe.



The project uses a webcam to detect hand landmarks and recognize different hand gestures. It also demonstrates how recognized gestures can be used to control computer functions.



\## Features



\- Real-time hand detection

\- 21-point hand landmark detection using MediaPipe

\- Finger counting

\- Left and right hand detection

\- Gesture recognition

\- OK gesture detection

\- Pointing direction detection

\- Thumbs-up detection

\- Windows volume control using hand gestures



\## Recognized Gestures



| Gesture | Recognition | Action |

|---|---|---|

| Fist | FIST | - |

| One finger | ONE | - |

| Peace | PEACE | - |

| Three fingers | THREE | - |

| Four fingers | FOUR | - |

| Open palm | OPEN PALM | - |

| Thumbs up | THUMBS UP | Increase volume |

| OK sign | OK | - |

| Point up | POINT UP | - |

| Point left | POINT LEFT | - |

| Point right | POINT RIGHT | - |



\## Technologies Used



\- Python 3.14

\- OpenCV

\- MediaPipe

\- Pycaw

\- Computer Vision



\## Project Structure



```text

HandGestureRecognition/

│

├── camera\_test.py

├── finger\_counter.py

├── hand\_detection.py

├── hand\_landmarker.task

├── requirements.txt

├── README.md

└── .gitignore

