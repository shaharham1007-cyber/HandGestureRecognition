import cv2
import mediapipe as mp
import math
import time

from pycaw.pycaw import AudioUtilities


# ============================================================
# FUNCTION 1: COUNT FINGERS
# ============================================================

def count_fingers(hand, hand_label):

    fingers = 0

    # -----------------------------
    # Thumb
    # -----------------------------

    if hand_label == "Right":

        if hand[4].x < hand[3].x:
            fingers += 1

    elif hand_label == "Left":

        if hand[4].x > hand[3].x:
            fingers += 1


    # -----------------------------
    # Index finger
    # -----------------------------

    if hand[8].y < hand[6].y:
        fingers += 1


    # -----------------------------
    # Middle finger
    # -----------------------------

    if hand[12].y < hand[10].y:
        fingers += 1


    # -----------------------------
    # Ring finger
    # -----------------------------

    if hand[16].y < hand[14].y:
        fingers += 1


    # -----------------------------
    # Little finger
    # -----------------------------

    if hand[20].y < hand[18].y:
        fingers += 1


    return fingers


# ============================================================
# FUNCTION 2: RECOGNIZE GESTURE
# ============================================================

def recognize_gesture(hand, fingers, hand_label):

    # ========================================================
    # OK GESTURE
    # ========================================================

    thumb_tip = hand[4]
    index_tip = hand[8]

    distance = math.sqrt(
        (thumb_tip.x - index_tip.x) ** 2 +
        (thumb_tip.y - index_tip.y) ** 2
    )

    middle_up = hand[12].y < hand[10].y
    ring_up = hand[16].y < hand[14].y
    little_up = hand[20].y < hand[18].y

    if distance < 0.08:

        if middle_up and ring_up and little_up:
            return "OK"


    # ========================================================
    # ONE FINGER / THUMBS UP / POINTING
    # ========================================================

    if fingers == 1:

        # -----------------------------
        # THUMBS UP
        # -----------------------------

        if hand[4].y < hand[3].y:
            return "THUMBS UP"


        # -----------------------------
        # INDEX FINGER DIRECTION
        # -----------------------------

        index_tip = hand[8]
        index_base = hand[5]

        dx = index_tip.x - index_base.x
        dy = index_tip.y - index_base.y


        # Pointing upward
        if abs(dy) > abs(dx) and dy < -0.15:
            return "POINT UP"


        # Pointing right
        elif abs(dx) > abs(dy) and dx > 0.15:
            return "POINT RIGHT"


        # Pointing left
        elif abs(dx) > abs(dy) and dx < -0.15:
            return "POINT LEFT"


        return "ONE"


    # ========================================================
    # OTHER GESTURES
    # ========================================================

    if fingers == 0:

        return "FIST"


    elif fingers == 2:

        return "PEACE"


    elif fingers == 3:

        return "THREE"


    elif fingers == 4:

        return "FOUR"


    elif fingers == 5:

        return "OPEN PALM"


    return "UNKNOWN"


# ============================================================
# WINDOWS VOLUME CONTROL
# ============================================================

last_volume_change = 0

device = AudioUtilities.GetSpeakers()

volume = device.EndpointVolume

# ============================================================
# MEDIAPIPE HAND DETECTOR
# ============================================================

BaseOptions = mp.tasks.BaseOptions

VisionRunningMode = mp.tasks.vision.RunningMode

HandLandmarker = mp.tasks.vision.HandLandmarker

HandLandmarkerOptions = (
    mp.tasks.vision.HandLandmarkerOptions
)


options = HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),

    running_mode=VisionRunningMode.VIDEO,

    num_hands=1
)


# ============================================================
# OPEN WEBCAM
# ============================================================

camera = cv2.VideoCapture(0)


# ============================================================
# START HAND DETECTION
# ============================================================

with HandLandmarker.create_from_options(options) as landmarker:

    timestamp = 0

    while True:

        # -----------------------------
        # Read camera
        # -----------------------------

        success, frame = camera.read()


        if not success:

            print("Could not access camera.")

            break


        # -----------------------------
        # Mirror camera
        # -----------------------------

        frame = cv2.flip(frame, 1)


        # -----------------------------
        # Convert BGR → RGB
        # -----------------------------

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # -----------------------------
        # Convert to MediaPipe image
        # -----------------------------

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )


        # -----------------------------
        # Detect hand
        # -----------------------------

        result = landmarker.detect_for_video(
            mp_image,
            timestamp
        )


        timestamp += 1


        # ====================================================
        # IF HAND IS DETECTED
        # ====================================================

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]


            # -----------------------------
            # Get Left / Right hand
            # -----------------------------

            hand_label = (
                result.handedness[0][0].category_name
            )


            # -----------------------------
            # Count fingers
            # -----------------------------

            fingers = count_fingers(
                hand,
                hand_label
            )


            # -----------------------------
            # Recognize gesture
            # -----------------------------

            gesture = recognize_gesture(
                hand,
                fingers,
                hand_label
            )


            # ====================================================
            # VOLUME CONTROL
            # ====================================================

            current_time = time.time()


            # -----------------------------
            # THUMBS UP = VOLUME UP
            # -----------------------------

            if gesture == "THUMBS UP":

                if current_time - last_volume_change > 1:

                    current_volume = (
                        volume.GetMasterVolumeLevelScalar()
                    )


                    new_volume = min(
                        current_volume + 0.05,
                        1.0
                    )


                    volume.SetMasterVolumeLevelScalar(
                        new_volume,
                        None
                    )


                    last_volume_change = current_time


            # ====================================================
            # DISPLAY FINGER COUNT
            # ====================================================

            cv2.putText(
                frame,

                f"Fingers: {fingers}",

                (30, 60),

                cv2.FONT_HERSHEY_SIMPLEX,

                1.2,

                (0, 255, 0),

                3
            )


            # ====================================================
            # DISPLAY HAND TYPE
            # ====================================================

            cv2.putText(
                frame,

                f"Hand: {hand_label}",

                (30, 110),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.9,

                (0, 255, 0),

                2
            )


            # ====================================================
            # DISPLAY GESTURE
            # ====================================================

            cv2.putText(
                frame,

                f"Gesture: {gesture}",

                (30, 160),

                cv2.FONT_HERSHEY_SIMPLEX,

                1.2,

                (0, 255, 0),

                3
            )


            # ====================================================
            # DRAW 21 HAND LANDMARKS
            # ====================================================

            for landmark in hand:

                x = int(
                    landmark.x * frame.shape[1]
                )

                y = int(
                    landmark.y * frame.shape[0]
                )


                cv2.circle(

                    frame,

                    (x, y),

                    5,

                    (0, 255, 0),

                    -1
                )


        # ====================================================
        # SHOW CAMERA
        # ====================================================

        cv2.imshow(
            "Hand Gesture Recognition",
            frame
        )


        # ====================================================
        # PRESS Q TO QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


# ============================================================
# CLOSE CAMERA
# ============================================================

camera.release()

cv2.destroyAllWindows()