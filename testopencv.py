import threading

import cv2
import numpy as np


def start_video_stream():
    print("Video-Stream starten")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print(
            "Fehler: Webcam konnte nicht geöffnet werden. Bitte überprüfen Sie die Zugriffsrechte und fügen Sie ggf. NSCameraUseContinuityCameraDeviceType zu Ihrer Info.plist hinzu, falls Continuity-Kameras verwendet werden.")
        return

    print("Webcam erfolgreich geöffnet. Drücken Sie 'q', um den Stream zu beenden.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fehler: Frame konnte nicht gelesen werden.")
                break

            # Bild in Graustufen konvertieren
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Kantenerkennung (Canny)
            edges = cv2.Canny(gray_frame, 100, 200)

            # Beide Bilder nebeneinander anzeigen
            combined_frame = np.hstack((frame, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)))
            cv2.putText(combined_frame, f"Battery: %", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(combined_frame, f"Height:  cm", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(combined_frame, f"Acceleration: (", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0), 2)
            # Beenden bei Tastendruck 'q'
            cv2.imshow("Video-Stream (Links: Original, Rechts: Kanten)", combined_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stream beendet durch Benutzereingabe.")
                break
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam freigegeben und alle Fenster geschlossen.")


if __name__ == "__main__":
    start_video_stream()
