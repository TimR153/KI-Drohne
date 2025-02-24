import threading
from djitellopy import Tello
from tensorflow.keras.models import load_model
import keyboard_control
import gesture_control
import drone_video

if __name__ == '__main__':
    try:
        global drone, run_flag

        drone = Tello()
        #drone.connect()
        run_flag.set()  # Setzt das Signal auf "True", damit die Threads laufen

        control_thread = threading.Thread(target=keyboard_control.control_drone, args=(drone, run_flag))
        video_thread = threading.Thread(target=drone_video.handle_video, args=(drone, run_flag))
        gesture_thread = threading.Thread(target=gesture_control, args=(drone, run_flag))

        #control_thread.start()
        #video_thread.start()
        gesture_thread.start()

        #control_thread.join()
        #video_thread.join()
        gesture_thread.join()

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")
