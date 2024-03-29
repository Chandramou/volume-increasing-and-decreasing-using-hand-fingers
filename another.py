import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=0, max_num_hands=True,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret, image = cap.read()
    if not ret:
        break

    video = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(video)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            if index_finger_y < thumb_y:
                hand_gesture = 'pointing up'
            elif index_finger_y > thumb_y:
                hand_gesture = 'pointing down'
            else:
                hand_gesture = 'other'

            if hand_gesture == 'pointing up':
                pyautogui.press('volumeup')
            elif hand_gesture == 'pointing down':
                pyautogui.press('volumedown')

    cv2.imshow('Hand Gesture',image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
