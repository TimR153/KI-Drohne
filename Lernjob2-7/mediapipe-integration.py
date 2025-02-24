import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2

BaseOptions = mp.tasks.BaseOptions # Objekt der BaseOptions-Klasse
HandLandmarker = mp.tasks.vision.HandLandmarker # Klasse, welche die Markierungspunkt-Erken-nung ausführt
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions # Klasse, welche die möglichenOptionen verarbeitet
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult # Klasse, die in einem 2D-Arraysdie Ergebnisse speichert
VisionRunningMode = mp.tasks.vision.RunningMode # Klasse, welche die Optionen entsprechenddem Modus einstellt
model_path = 'Aufgabe3a/hand_landmarker.task'  # Der absolute Pfad zum vortrainierten Modell
mp_results = None # Leere Variable zum Speichern der Ergebnisse der Handpunkterkennung