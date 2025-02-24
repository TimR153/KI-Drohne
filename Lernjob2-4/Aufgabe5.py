from asyncio import sleep

from djitellopy import Tello
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

        forward_backward = 0
        left_right = 0
        up_down = 0
        yaw = 0

        drone.streamoff()
        sleep(0.5)
        drone.streamon()

        while run:
            try:
                frame = drone.get_frame_read().frame
                if frame is not None:
                    frame = cv2.resize(frame, (360, 240))
                    cv2.imshow("Drohnenansicht", frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('m'):
                    drone.turn_motor_on()
                    print("Motor  gestartet.")

                if key == ord('n'):
                    drone.turn_motor_off()
                    print("Motor  aus.")

                if key == ord('t'):
                    drone.takeoff()
                    print("Drohne gestartet.")

                elif key == ord('l'):
                    drone.land()
                    print("Drohne gelandet.")

                elif key == ord('e'):
                    drone.emergency()
                    print("Drohne gestoppt.")
                    run = False

                elif key == ord('w'):
                    forward_backward = 30

                elif key == ord('s'):
                    forward_backward = -30

                elif key == ord('a'):
                    left_right = -30

                elif key == ord('d'):
                    left_right = 30

                elif key == ord(' '):
                    up_down = 30

                elif key == ord('z'):
                    up_down = -30

                elif key == ord('q'):
                    yaw = -30

                elif key == ord('e'):
                    yaw = 30

                elif key == ord('x'):
                    forward_backward = 0
                    left_right = 0
                    up_down = 0
                    yaw = 0

                elif key == ord('i'):
                    drone.flip_forward()
                    print("Flip vorwärts.")

                elif key == ord('k'):
                    drone.flip_back()
                    print("Flip rückwärts.")

                elif key == ord('j'):
                    drone.flip_left()
                    print("Flip nach links.")

                elif key == ord('l'):
                    drone.flip_right()
                    print("Flip nach rechts.")

                elif key == ord('b'):
                    run = False

            except Exception as e:
                print(f"Fehler: {e}")
                drone.land()
                break

        drone.streamoff()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Fehler beim Starten des Programms: {e}")

    finally:
        if 'drone' in locals():
            drone.land()
        print("Programm beendet.")


if __name__ == '__main__':
    main()
