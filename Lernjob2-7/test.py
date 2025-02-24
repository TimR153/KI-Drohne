import cv2
import mediapipe as mp
import video_helper

# MediaPipe initialisieren
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Kamera starten
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Bild spiegeln & in RGB konvertieren
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand erkennen
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Landmarken auslesen
            landmarks = hand_landmarks.landmark

            # Daumenpunkte
            thumb_tip = landmarks[4]  # Daumenspitze
            thumb_base = landmarks[2]  # Daumenbasis (näher an der Handfläche)

            # X- und Y-Koordinaten
            dx = thumb_tip.x - thumb_base.x
            dy = thumb_tip.y - thumb_base.y

            # Daumenrichtung bestimmen
            if abs(dx) > abs(dy):  # Bewegung entlang der X-Achse
                if dx > 0:
                    direction = "Daumen nach rechts"
                else:
                    direction = "Daumen nach links"
            else:  # Bewegung entlang der Y-Achse
                if dy > 0:
                    direction = "Daumen nach unten"
                else:
                    direction = "Daumen nach oben"

            # Text auf dem Frame anzeigen
            cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Bild anzeigen
    image = video_helper.resize_and_crop(frame, (480, 480))
    cv2.imshow("Daumen Richtungserkennung", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Aufräumen
cap.release()
cv2.destroyAllWindows()
