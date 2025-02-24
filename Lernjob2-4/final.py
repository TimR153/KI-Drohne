import time
from djitellopy import Tello
import cv2
from pynput import keyboard


def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")


def print_height(drone):
    height = drone.get_height()
    print(f"H\u00f6he: {height} cm.")


def main():
    try:
        first = False
        run = True
        drone = Tello()
        drone.connect()
        print_battery_status(drone)
        print_height(drone)

        # Dictionary to track key presses
        keys_pressed = {
            'up_down': 0,
            'forward_backward': 0,
            'left_right': 0,
            'yaw': 0
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
                    nonlocal run
                    run = False
                    drone.land()
                    print("Drohne gelandet.")
                elif key.char == 'c':
                    print("Drohne gestartet.")
                    drone.takeoff()
                elif key.char == 'm':
                    drone.turn_motor_on()
                elif key.char == 'n':
                    drone.turn_motor_off()
                elif key.char == 'v':
                    run = False
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
                elif key.char == 't':
                    keys_pressed['up_down'] = 50
                elif key.char == 'g':
                    keys_pressed['up_down'] = -50
                elif key.char == 'q':
                    keys_pressed['yaw'] = -50
                elif key.char == 'e':
                    keys_pressed['yaw'] = 50
                elif key.char == 'x':
                    drone.streamoff()
                elif key.char == 'i':
                    drone.flip_forward()
                elif key.char == 'k':
                    drone.flip_back()
                elif key.char == 'j':
                    drone.flip_left()
                elif key.char == 'l':
                    drone.flip_right()
                send_control()
            except AttributeError:
                pass

        def on_release(key):
            try:
                if key.char in ('w', 's'):
                    keys_pressed['forward_backward'] = 0
                elif key.char in ('a', 'd'):
                    keys_pressed['left_right'] = 0
                elif key.char == ' ':
                    keys_pressed['up_down'] = 0
                elif key.char == 'z':
                    keys_pressed['up_down'] = 0
                elif key.char in ('q', 'e'):
                    keys_pressed['yaw'] = 0
                send_control()
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        while run:
            try:
                if not first:
                    drone.takeoff()
                    time.sleep(1)
                    first = True
                    drone.streamoff()
                    time.sleep(0.5)
                    drone.streamon()

                img = drone.get_frame_read().frame
                if img is None:
                    print("Kein Bild vom Stream erhalten")
                img = cv2.resize(img, (360, 240))
                cv2.imshow("Image", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print(f"Fehler im Run-Loop: {e}")
                drone.land()
                break

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")


if __name__ == '__main__':
    main()
