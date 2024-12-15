from asyncio import sleep

from djitellopy import Tello
from pynput import keyboard
import cv2


def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")


def print_height(drone):
    height = drone.get_height()
    print(f"Höhe: {height} cm.")


def main():
    try:
        run = True
        drone = Tello()
        drone.connect()
        print_battery_status(drone)
        print_height(drone)

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
            nonlocal run
            try:
                if key.char == 'b':
                    run = False
                    drone.land()
                    print("Drohne gelandet.")
                elif key.char == 't':
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
                elif key.char == ' ':  # Space key
                    keys_pressed['up_down'] = 50
                elif key == keyboard.Key.shift:
                    keys_pressed['up_down'] = -50
                elif key.char == 'q':
                    keys_pressed['yaw'] = -50
                elif key.char == 'e':
                    keys_pressed['yaw'] = 50
                elif key.char == 'i':
                    drone.flip_forward()
                elif key.char == 'k':
                    drone.flip_back()
                elif key.char == 'j':
                    drone.flip_left()
                elif key.char == 'l':
                    drone.flip_right()
                elif key.char == 't':
                    drone.streamoff()
                    sleep(0.5)
                    drone.streamon()
                    img = drone.get_frame_read().frame
                    img = cv2.resize(img, (360, 240))
                    cv2.imshow("Image", img)
                elif key.char == 'g':
                    drone.streamoff()
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
            if key == keyboard.Key.esc:
                nonlocal run
                run = False
                return False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while run:
                listener.join(0.1)

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")


if __name__ == '__main__':
    main()
