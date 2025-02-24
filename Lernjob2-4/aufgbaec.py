import time
from djitellopy import Tello
import cv2
#das klappt
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
                print("Kamera")
                img = cv2.resize(img, (360, 240))
                cv2.imshow("Image", img)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('b'):  # 'b' for land
                    run = False
                    drone.land()
                    print("Drohne gelandet.")
                elif key == ord('t'):  # 't' for takeoff
                    drone.takeoff()
                elif key == ord('m'):  # 'm' for turning motor on
                    drone.turn_motor_on()
                elif key == ord('n'):  # 'n' for turning motor off
                    drone.turn_motor_off()
                elif key == ord('v'):  # 'v' for emergency
                    run = False
                    drone.emergency()
                    print("Notfall beendet.")
                elif key == ord('w'):  # 'w' for forward
                    keys_pressed['forward_backward'] = 50
                elif key == ord('s'):  # 's' for backward
                    keys_pressed['forward_backward'] = -50
                elif key == ord('a'):  # 'a' for left
                    keys_pressed['left_right'] = -50
                elif key == ord('d'):  # 'd' for right
                    keys_pressed['left_right'] = 50
                elif key == ord(' '):  # Space for up
                    keys_pressed['up_down'] = 50
                elif key == ord('z'):  # Shift for down
                    keys_pressed['up_down'] = -50
                elif key == ord('q'):  # 'q' for yaw left
                    keys_pressed['yaw'] = -50
                elif key == ord('e'):  # 'e' for yaw right
                    keys_pressed['yaw'] = 50
                elif key == ord('i'):  # 'i' for flip forward
                    drone.flip_forward()
                elif key == ord('k'):  # 'k' for flip back
                    drone.flip_back()
                elif key == ord('j'):  # 'j' for flip left
                    drone.flip_left()
                elif key == ord('l'):  # 'l' for flip right
                    drone.flip_right()
                elif key == ord('x'):  # 'x' for stopping stream
                    drone.streamoff()


                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                    break

            except Exception as e:
                print(f"Fehler im Run-Loop: {e}")
                # Optional: Drohne sicher landen im Falle eines Fehlers
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
