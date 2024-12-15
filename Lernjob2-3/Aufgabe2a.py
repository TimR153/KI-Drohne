import djitellopy as tello
import keyboard
import time


def handle_inputs(drone):
    print("Steuerung aktiv. Drücke 'b' zum Beenden.")

    # Hotkeys für Drohnensteuerung
    keyboard.add_hotkey('space', lambda:  drone.move_up(30))
    keyboard.add_hotkey('shift', lambda:  drone.move_down(30))
    keyboard.add_hotkey('w', lambda: drone.move_forward(30))
    keyboard.add_hotkey('s', lambda: drone.move_back(30))
    keyboard.add_hotkey('a', lambda: drone.move_left(30))
    keyboard.add_hotkey('d', lambda: drone.move_right(30))
    keyboard.add_hotkey('i', lambda: drone.flip_forward())
    keyboard.add_hotkey('k', lambda:  drone.flip_back())
    keyboard.add_hotkey('j', lambda: drone.flip_left())
    keyboard.add_hotkey('l', lambda: drone.flip_right())
    keyboard.add_hotkey('v', lambda: drone.land())
    keyboard.add_hotkey('b', lambda: exit_program(drone))
    keyboard.add_hotkey('p', lambda: print_battery_status(drone))

    while True:
        time.sleep(0.1)


def print_battery_status(drone):
    battery = drone.get_battery()
    print(f"Akkustand: {battery}%.")


def exit_program(drone):
    print("Beenden-Taste (b) erkannt. Drohne landet...")
    drone.land()
    print("Programm beendet.")
    exit(0)


def main():
    try:
        drone = tello.Tello()
        drone.connect()
        print_battery_status(drone)
        drone.set_speed()

        handle_inputs(drone)

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if 'drone' in locals():
            print("Notlandung der Drohne...")
            drone.land()
        print("Programm beendet.")


if __name__ == '__main__':
    main()
