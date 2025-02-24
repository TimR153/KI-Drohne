import djitellopy as tello
import keyboard


def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")


def print_height(drone):
    height = drone.get_height()
    print(f"Hoehe: {height}%.")


def main():
    try:
        run = True
        drone = tello.Tello()
        drone.connect()
        print_battery_status(drone)
        print_height(drone)

        while run:
            if keyboard.is_pressed('b'):
                run = False
                drone.land()
                print("Drohne gelandet.")
            if keyboard.is_pressed('v'):
                run = False
                drone.emergency()
                print("Emergency beendet")
            if keyboard.is_pressed('space'):
                drone.move_up(1)
            if keyboard.is_pressed('shift'):
                drone.move_down(1)
            if keyboard.is_pressed('w'):
                drone.move_forward(1)
            if keyboard.is_pressed('s'):
                drone.move_back(1)
            if keyboard.is_pressed('a'):
                drone.move_left(1)
            if keyboard.is_pressed('d'):
                drone.move_right(1)
            if keyboard.is_pressed('q'):
                drone.rotate_clockwise(-1)
            if keyboard.is_pressed('e'):
                drone.rotate_clockwise(1)
            if keyboard.is_pressed('i'):
                drone.flip_forward()
            if keyboard.is_pressed('k'):
                drone.flip_back()
            if keyboard.is_pressed('j'):
                drone.flip_left()
            if keyboard.is_pressed('l'):
                drone.flip_right()

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")


if __name__ == '__main__':
    main()



