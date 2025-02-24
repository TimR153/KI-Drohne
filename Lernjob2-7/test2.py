import cv2
import mediapipe as mp
import time  # Importiere time für Zeitstempel

# MediaPipe Gesture Recognizer initialisieren
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Callback-Funktion für Live-Stream-Modus
def gesture_callback(result, image, timestamp_ms):
    """Verarbeitet die Ergebnisse des Gesture Recognizers"""
    global detected_gesture
    if result.gestures:
        detected_gesture = result.gestures[0][0].category_name
    else:
        detected_gesture = None

# Gesture Recognizer konfigurieren
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path="gesture_recognizer.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=gesture_callback  # Callback-Funktion übergeben
)

# Kamera starten
cap = cv2.VideoCapture(1)

detected_gesture = None  # Variable zum Speichern der aktuellen Geste

with GestureRecognizer.create_from_options(options) as recognizer:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Bild spiegeln
        frame = cv2.flip(frame, 1)

        # OpenCV zu MediaPipe-Bild konvertieren
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Zeitstempel in Millisekunden basierend auf der aktuellen Systemzeit
        timestamp = int(time.time() * 1000)

        # Gestenerkennung aufrufen
        recognizer.recognize_async(mp_image, timestamp)

        # Falls eine Geste erkannt wurde, anzeigen
        if detected_gesture:
            cv2.putText(frame, f"Geste: {detected_gesture}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Bild anzeigen
        cv2.imshow("Gestenerkennung", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Aufräumen
cap.release()
cv2.destroyAllWindows()
