import cv2


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