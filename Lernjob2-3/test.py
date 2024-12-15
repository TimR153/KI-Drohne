from pynput import keyboard

def on_press(key):
    try:
        print(f"Taste gedrückt: {key.char}")
    except AttributeError:
        print(f"Spezialtaste gedrückt: {key}")

def on_release(key):
    print(f"Taste losgelassen: {key}")
    # Beende das Skript, wenn die ESC-Taste losgelassen wird
    if key == keyboard.Key.esc:
        print("Beenden...")
        return False

# Listener für Tastenanschläge starten
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Drücke Tasten, um sie zu testen. Drücke ESC zum Beenden.")
    listener.join()
