import cv2
import numpy as np


def rgb_to_bgr(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR
    )


def bgr_to_rgb(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )