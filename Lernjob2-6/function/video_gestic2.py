from tensorflow.keras.models import load_model
import cv2
import numpy as np
from djitellopy import Tello
np.set_printoptions(suppress=True)


def resize_and_crop(image, target_size):
    """
    Resizes an image while maintaining the aspect ratio, and crops it to the target size.
    :param image: Input image from OpenCV (numpy array).
    :param target_size: Tuple of (width, height) for the output image.
    :return: Resized and cropped image.
    """
    target_width, target_height = target_size
    original_height, original_width = image.shape[:2]

    # Compute the scaling factor for resizing
    scale = max(target_width / original_width, target_height / original_height)

    # Resize the image while keeping the aspect ratio
    resized_width = int(original_width * scale)
    resized_height = int(original_height * scale)
    resized_image = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_AREA)

    # Crop the center of the image
    start_x = (resized_width - target_width) // 2
    start_y = (resized_height - target_height) // 2
    cropped_image = resized_image[start_y:start_y + target_height, start_x:start_x + target_width]

    return cropped_image

global drone, run_flag


model = load_model("/Users/timrentrop/Desktop/KI Drohne/Lernjob2-6/keras_Model.h5", compile=False)
model.save("saved_model/")
# Load the labels
class_names = open("/Users/timrentrop/Desktop/KI Drohne/Lernjob2-6/labels.txt", "r").readlines()
# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(1)
while True:
    # Grab the webcamera's image.
    ret, image = camera.read()
    # Resize the raw image into (224-height,224-width) pixels
    image = resize_and_crop(image, (224, 224))
    # Show the image in a window
    cv2.imshow("Webcam Image", image)
    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1
    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    # Print prediction and confidence score
    if confidence_score > 0.99:
        if "up" in class_name:
            print("Gesture 'up' detected, making the drone ascend.")
            # drone.send_rc_control(0, 0, 50, 0)
        elif "down" in class_name:
            print("Gesture 'down' detected, making the drone descend.")
            # drone.send_rc_control(0, 0, -50, 0)
        elif "left" in class_name:
            print("Gesture 'left' detected, making the drone move left.")
            # drone.send_rc_control(0, 50, 0, 0)
        elif "right" in class_name:
            print("Gesture 'right' detected, making the drone move right.")
        # drone.send_rc_control(0, -50, 0, 0)

        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
camera.release()
cv2.destroyAllWindows()
