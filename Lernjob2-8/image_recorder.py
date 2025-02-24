from datetime import datetime
import cv2
import time
import os

directory = "/Users/timrentrop/Desktop/KI Drohne/Lernjob2-8/trainingData"
folder_name = input("Gib den Ordnernamen ein, in dem die Bilder gespeichert werden sollen: ")

folder_path = f"{directory}/{folder_name}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Ordner '{folder_path}' wurde erstellt.")

cap = cv2.VideoCapture(1)

print("Drücke die Leertaste, um ein Bild aufzunehmen. Drücke 'q', um das Programm zu beenden.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Fehler beim Lesen des Bildes von der Kamera.")
        break

    cv2.imshow("Kamera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 32:
        timestamp = time.time()
        image_name = f"Image_{timestamp}.jpg"
        image_path = os.path.join(folder_path, image_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f'{folder_path}/Image_{timestamp}.jpg', frame)
        print(f"Bild gespeichert: {image_path}")
    elif key == ord('q'):
        print("Programm beendet.")
        break

cap.release()
cv2.destroyAllWindows()
