import mediapipe as mp
import cv2
import video_helper

timestamp = 0
global drone, run_flag

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode
model_path = 'gesture_recognizer.task'

detected_gesture = None

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


def gesture_callback(result, image, timestamp_ms):
    global detected_gesture
    if result.gestures:
        detected_gesture = result.gestures[0][0].category_name
    else:
        detected_gesture = None


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # print('gesture recognition result: {}'.format(result))
    # Falls eine Geste erkannt wurde ...
    if result.gestures.__len__() != 0:
        print(result.gestures[0][0].category_name) # gebe auf der Konsole die erkannte Geste aus


options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=gesture_callback)


def start(drone, run_flag):
    global timestamp
    global options
    camera = cv2.VideoCapture(1)

    with GestureRecognizer.create_from_options(options) as recognizer:
        while True:
            timestamp += 1
            status, frame = camera.read()
            frame = video_helper.resize_and_crop(frame, (480, 480))
            frame = cv2.flip(frame, 1)
            if detected_gesture:
                cv2.putText(frame, f"Geste: {detected_gesture}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if detected_gesture == "Thumb_Up":
                    keys_pressed['up_down'] = 50
                if detected_gesture == "Thumb_Down":
                    keys_pressed['up_down'] = -50
                send_control()
            cv2.imshow('Show', frame)
            if cv2.waitKey(1) == 27:
                break
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            recognizer.recognize_async(mp_image, timestamp)