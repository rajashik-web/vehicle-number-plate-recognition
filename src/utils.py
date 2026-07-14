import cv2
import numpy as np
import re


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
    


def normalize_plate(text):
    """
    Normalize OCR output.

    Example:
        mh20 ej 0364
        ↓
        MH20EJ0364
    """

    if text is None:
        return ""

    text = text.upper()

    text = text.replace(" ", "")
    text = text.replace("-", "")

    return text


def is_valid_plate(text):
    """
    Validate Indian vehicle registration number.
    """

    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"

    return re.match(pattern, text) is not None