import cv2
import numpy as np


class PlatePreprocessor:

    def process(self, image):

        # -------------------------
        # Resize
        # -------------------------

        image = cv2.resize(
            image,
            None,
            fx=4,
            fy=4,
            interpolation=cv2.INTER_CUBIC
        )

        # -------------------------
        # Gray
        # -------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # -------------------------
        # Bilateral Filter
        # -------------------------

        gray = cv2.bilateralFilter(
            gray,
            11,
            17,
            17
        )

        # -------------------------
        # CLAHE
        # -------------------------

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        gray = clahe.apply(gray)

        # -------------------------
        # Sharpen
        # -------------------------

        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        sharp = cv2.filter2D(
            gray,
            -1,
            kernel
        )

        # -------------------------
        # Adaptive Threshold
        # -------------------------

        binary = cv2.adaptiveThreshold(
            sharp,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            15
        )

        return binary