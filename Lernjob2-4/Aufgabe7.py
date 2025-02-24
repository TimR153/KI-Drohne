import cv2
from djitellopy import Tello
from threading import Thread
import time
import keyboard

def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")

def print_height(drone):
    height = drone.get_height()
    print(f"Höhe: {height} cm.")

def video_stream(drone, run_flag):
    drone.streamoff()
    time.sleep(0.5)
    drone.streamon()

    while run_flag[0]:
        frame = drone.get_frame_read().frame
        if frame is not None:
            frame = cv2.resize(frame, (360, 240))
            cv2.imshow("Drohnenansicht", frame)

        if keyboard.is_pressed('b'):
            run_flag[0] = False
            break

    drone.streamoff()
    cv2.destroyAllWindows()

def control_drone(drone, run_flag):
    while run_flag[0]:

        if keyboard.is_pressed('t'):
            drone.takeoff()
            print("Drohne gestartet.")

        elif keyboard.is_pressed('l'):
            drone.land()
            print("Drohne gelandet.")
            run_flag[0] = False

        elif keyboard.is_pressed('e'):
            drone.emergency()
            print("Drohne gestoppt.")
            run_flag[0] = False

        elif keyboard.is_pressed('w'):
            drone.send_rc_control(0, 30, 0, 0)

        elif keyboard.is_pressed('s'):
            drone.send_rc_control(0, -30, 0, 0)

        elif keyboard.is_pressed('a'):
            drone.send_rc_control(-30, 0, 0, 0)

        elif keyboard.is_pressed('d'):
            drone.send_rc_control(30, 0, 0, 0)

        elif keyboard.is_pressed('space'):
            drone.send_rc_control(0, 0, 30, 0)

        elif keyboard.is_pressed('z'):
            drone.send_rc_control(0, 0, -30, 0)

        elif keyboard.is_pressed('q'):
            drone.send_rc_control(0, 0, 0, -30)

        elif keyboard.is_pressed('e'):
            drone.send_rc_control(0, 0, 0, 30)

        elif keyboard.is_pressed('x'):
            drone.send_rc_control(0, 0, 0, 0)

        elif keyboard.is_pressed('i'):
            drone.flip_forward()
            print("Flip vorwärts.")

        elif keyboard.is_pressed('k'):
            drone.flip_back()
            print("Flip rückwärts.")

        elif keyboard.is_pressed('j'):
            drone.flip_left()
            print("Flip nach links.")

        elif keyboard.is_pressed('o'):
            drone.flip_right()
            print("Flip nach rechts.")

        time.sleep(0.1)

def main():
    try:
        run_flag = [True]

        drone = Tello()
        drone.connect()
        print_battery_status(drone)
        print_height(drone)

        video_thread = Thread(target=video_stream, args=(drone, run_flag))
        control_thread = Thread(target=control_drone, args=(drone, run_flag))

        video_thread.start()
        control_thread.start()

        video_thread.join()
        control_thread.join()

    except Exception as e:
        print(f"Fehler beim Starten des Programms: {e}")

    finally:
        if 'drone' in locals():
            drone.land()
        print("Programm beendet.")

if __name__ == '__main__':
    main()
