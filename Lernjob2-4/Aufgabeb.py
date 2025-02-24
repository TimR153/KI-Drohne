import time
from djitellopy import Tello
import cv2
import keyboard

def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")

def print_height(drone):
    height = drone.get_height()
    print(f"Höhe: {height} cm.")

def main():

    try:
        first = False
        run = True
        drone = Tello()
        drone.connect()
        print_battery_status(drone)
        print_height(drone)

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

        while run:
            try:
                if not first:
                    first = True
                    drone.streamoff()
                    time.sleep(0.5)
                    drone.streamon()

                img = drone.get_frame_read().frame
                if img is not None:
                    img = cv2.resize(img, (360, 240))
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

                # Controls for drone
                if keyboard.is_pressed('esc'):
                    run = False
                    break

                if keyboard.is_pressed('N'):
                    run = False
                    drone.land()
                    print("Drohne gelandet.")
                if keyboard.is_pressed('t'):
                    drone.takeoff()
                if keyboard.is_pressed('w'):
                    keys_pressed['forward_backward'] = 50
                elif keyboard.is_pressed('s'):
                    keys_pressed['forward_backward'] = -50
                else:
                    keys_pressed['forward_backward'] = 0

                if keyboard.is_pressed('a'):
                    keys_pressed['left_right'] = -50
                elif keyboard.is_pressed('d'):
                    keys_pressed['left_right'] = 50
                else:
                    keys_pressed['left_right'] = 0

                if keyboard.is_pressed('space'):
                    keys_pressed['up_down'] = 50
                elif keyboard.is_pressed('shift'):
                    keys_pressed['up_down'] = -50
                else:
                    keys_pressed['up_down'] = 0

                if keyboard.is_pressed('q'):
                    keys_pressed['yaw'] = -50
                elif keyboard.is_pressed('e'):
                    keys_pressed['yaw'] = 50
                else:
                    keys_pressed['yaw'] = 0

                send_control()

            except Exception as e:
                print(f"Fehler: {e}")

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")

if __name__ == '__main__':
    keyboard._.setup_tables()
    main()
