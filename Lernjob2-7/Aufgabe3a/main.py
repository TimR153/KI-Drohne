import mediapipe as mp # Importiert das MediaPipe-Framework, dessen Methoden wir über mp. nutzen
from mediapipe import solutions # Stellt uns alle Klassen und Methoden von solution in MediaPipezur verfügung
from mediapipe.framework.formats import landmark_pb2 # Ermöglicht das Zeichnen von Markie-rungen in Bilder
import numpy as np # Die numpy-Bibliothek
import cv2 # Die opencv-python – Bibliothek
from mediapipe.tasks.python.components.containers import landmark
import video_helper

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green
timestamp = 0

BaseOptions = mp.tasks.BaseOptions # Objekt der BaseOptions-Klasse
HandLandmarker = mp.tasks.vision.HandLandmarker # Klasse, welche die Markierungspunkt-Erken-nung ausführt
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions # Klasse, welche die möglichenOptionen verarbeitet
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult # Klasse, die in einem 2D-Arraysdie Ergebnisse speichert
VisionRunningMode = mp.tasks.vision.RunningMode # Klasse, welche die Optionen entsprechenddem Modus einstellt
model_path = 'hand_landmarker.task' # Der absolute Pfad zum vortrainierten Modell
mp_results = None # Leere Variable zum Speichern der Ergebnisse der Handpunkterkennung

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global mp_results # Globale Variable verfügbar machen
    # Falls wir Handmarkierungspunkte erkannt haben ...
    if result.handedness.__len__() != 0:
        print(result.handedness[0][0].display_name) # gebe auf der Konsole die erkannte Hand aus
    mp_results = result # Speichern der Ergebnisse in der globalen Variable

options = HandLandmarkerOptions(
base_options=BaseOptions(model_asset_path=model_path), # Pfad zum vortrainierten Modell
running_mode=VisionRunningMode.LIVE_STREAM, # Erkennungsmodus (Bild, Video, Stream)
result_callback=print_result) # Festlegen der Funktion, welche die Ergebnisse verarbeitet

# Funktion zum Zeichnen von Handmarkierungspunkten auf das Bild
def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image


if __name__ == '__main__':
    with HandLandmarker.create_from_options(options) as landmarker:
        # Bild der Kamera dauerhaft abfangen
        while True:
            # Abfangen des aktuellen Frames
            camera = cv2.VideoCapture(1)
            status, frame = camera.read()  # status = Boolean (true, wenn Frame erkannt wurde), frame = Bild- datei
            # Bild auf die benötigte Größe zurechtschneiden
            frame = video_helper.resize_and_crop(frame, (480, 480))
            # Bild vertikal um 180° drehen
            frame = cv2.flip(frame, 1)
            cv2.imshow('Show', frame)
            # Wenn die Taste ESC gedrückt wird, beende die Schleife
            if cv2.waitKey(1) == 27:
                break
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # versucht auf dem Frame die Handmarkierungspunkte zu erkennen
            landmarker.detect_async(mp_image, timestamp)
            timestamp+= 1
            if not (mp_results is None):
                processed_image = draw_landmarks_on_image(mp_image.numpy_view(), mp_results)
                cv2.imshow('Show', processed_image)
            else:
                cv2.imshow('Show', frame)