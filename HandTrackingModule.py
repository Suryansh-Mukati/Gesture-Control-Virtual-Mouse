import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Screen size for mapping gestures
screen_width, screen_height = pyautogui.size()

# Cooldown timers for clicks
last_left_click_time = 0
last_right_click_time = 0
click_cooldown = 0  # 500 ms cooldown

# Drag state
dragging = False  # Track if dragging is active

# Initialize Pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Helper function to calculate Euclidean distance
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Variables for smoothing mouse movement
prev_screen_x, prev_screen_y = 0, 0
alpha = 0.8  # Smoothing factor

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame
    h, w, c = frame.shape

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            # Identify if the hand is left or right
            hand_label = result.multi_handedness[idx].classification[0].label

            # Get landmarks for gestures
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_base = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_base = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

            # Get landmarks for gestures
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Map hand coordinates to screen coordinates
            x = index_tip.x * w
            y = index_tip.y * h
            screen_x = int((x / w) * screen_width)
            screen_y = int((y / h) * screen_height)

            # Smooth cursor movement
            screen_x = int(alpha * prev_screen_x + (1 - alpha) * screen_x)
            screen_y = int(alpha * prev_screen_y + (1 - alpha) * screen_y)
            pyautogui.moveTo(screen_x, screen_y)

            # Update previous coordinates
            prev_screen_x, prev_screen_y = screen_x, screen_y

            # Calculate distances for gestures
            index_middle_distance = calculate_distance(index_tip, middle_tip)
            index_thumb_distance = calculate_distance(index_tip, thumb_tip)

            current_time = time.time()

            # Left-click when index and middle fingers touch
            if index_middle_distance < 0.03:  # Adjust threshold for better accuracy
                if current_time - last_left_click_time > click_cooldown:
                    pyautogui.click()
                    print("Left Click")
                    last_left_click_time = current_time

            # Right-click when index finger and thumb touch
            elif index_thumb_distance < 0.03:  # Adjust threshold for better accuracy
                if current_time - last_right_click_time > click_cooldown:
                    pyautogui.rightClick()
                    print("Right Click")
                    last_right_click_time = current_time

             # Check if the hand forms a fist (all fingers curled in)
            is_fist = (
                index_tip.y > index_base.y
                and middle_tip.y > middle_base.y
                and ring_tip.y > ring_base.y
                and pinky_tip.y > pinky_base.y
                and calculate_distance(thumb_tip, thumb_base) < 0.05
            )

            # Drag and Drop using fist gesture
            if is_fist and not dragging:
                pyautogui.mouseDown()  # Hold left mouse button
                dragging = True
                print("Drag Started")
            elif not is_fist and dragging:
                pyautogui.mouseUp()  # Release left mouse button
                dragging = False
                print("Drag Ended")

            # Volume and Brightness control if left hand is detected
            if hand_label == "Left":
                index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                index_tip_y = index_tip.y
                base_y = index_base.y

                # Volume control: Adjust volume based on the vertical movement of the index finger
                volume_level = np.interp(index_tip_y, [0, 1], [1.0, 0.0])  # Normalize Y to volume range
                volume.SetMasterVolumeLevelScalar(volume_level, None)
                print(f"Volume: {int(volume_level * 100)}%")

                # Brightness control: Use thumb position relative to the screen height
                brightness_level = np.interp(thumb_tip.y, [0, 1], [100, 0])  # Normalize Y to brightness range
                sbc.set_brightness(int(brightness_level))
                print(f"Brightness: {int(brightness_level)}%")

            # Draw landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Virtual Mouse with Gestures", frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
