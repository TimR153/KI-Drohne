import threading
import time
from djitellopy import Tello
from pynput import keyboard
import cv2


def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")


def print_height(drone):
    height = drone.get_height()
    print(f"Höhe: {height} cm.")


def handle_video(drone, run_flag):
    """Stream and display video frames from the drone."""
    drone.streamoff()
    drone.streamon()
    while run_flag.is_set():
        frame = drone.get_frame_read().frame
        if frame is not None:
            cv2.imshow("Tello Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Kein Bild vom Stream erhalten.")
    drone.streamoff()
    cv2.destroyAllWindows()


def control_drone(drone, run_flag):
    """Handle drone controls based on keyboard input."""
    # Dictionary to track multiple key presses
    keys_pressed = {
        'up_down': 0,  # Up/Down movement
        'forward_backward': 0,  # Forward/Backward movement
        'left_right': 0,  # Left/Right movement
        'yaw': 0  # Rotation
    }

    def send_control():
        drone.send_rc_control(
            keys_pressed['left_right'],
            keys_pressed['forward_backward'],
            keys_pressed['up_down'],
            keys_pressed['yaw']
        )

    def on_press(key):
        try:
            if key.char == 'b':
                run_flag.clear()
                drone.land()
                print("Drohne gelandet.")
            elif key.char == 't':
                drone.takeoff()
            elif key.char == 'v':
                run_flag.clear()
                drone.emergency()
                print("Notfall beendet.")
            elif key.char == 'w':
                keys_pressed['forward_backward'] = 50
            elif key.char == 's':
                keys_pressed['forward_backward'] = -50
            elif key.char == 'a':
                keys_pressed['left_right'] = -50
            elif key.char == 'd':
                keys_pressed['left_right'] = 50
            elif key.char == ' ':  # Space key
                keys_pressed['up_down'] = 50
            elif key == keyboard.Key.shift:
                keys_pressed['up_down'] = -50
            elif key.char == 'q':
                keys_pressed['yaw'] = -50
            elif key.char == 'e':
                keys_pressed['yaw'] = 50
            send_control()
        except AttributeError:
            pass
        except Exception as e:
            print(f"Fehler bei der Verarbeitung der Taste: {e}")

    def on_release(key):
        try:
            if key.char in ['w', 's']:
                keys_pressed['forward_backward'] = 0
            elif key.char in ['a', 'd']:
                keys_pressed['left_right'] = 0
            elif key.char == ' ':
                keys_pressed['up_down'] = 0
            elif key == keyboard.Key.shift:
                keys_pressed['up_down'] = 0
            elif key.char in ['q', 'e']:
                keys_pressed['yaw'] = 0
            send_control()
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while run_flag.is_set():
            listener.join(0.1)


if __name__ == '__main__':
    try:
        drone = Tello()
        drone.connect()

        print_battery_status(drone)
        print_height(drone)

        # Shared flag to control the threads
        run_flag = threading.Event()
        run_flag.set()

        # Create and start the threads
        control_thread = threading.Thread(target=control_drone, args=(drone, run_flag))
        video_thread = threading.Thread(target=handle_video, args=(drone, run_flag))

        control_thread.start()
        video_thread.start()

        # Wait for the threads to finish
        control_thread.join()
        video_thread.join()

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")
