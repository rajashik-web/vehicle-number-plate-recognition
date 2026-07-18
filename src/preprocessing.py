import cv2
import numpy as np


class PlatePreprocessor:

    def generate_variants(self, image):
        """
        Generate multiple versions of the same plate image.
        Each version is optimized for different lighting conditions.
        """

        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        variants = []

        # ------------------------------------------------
        # Variant 1
        # Original grayscale
        # ------------------------------------------------

        variants.append(gray)

        # ------------------------------------------------
        # Variant 2
        # CLAHE
        # ------------------------------------------------

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        clahe_img = clahe.apply(gray)

        variants.append(clahe_img)

        # ------------------------------------------------
        # Variant 3
        # Adaptive Threshold
        # ------------------------------------------------

        threshold = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            15
        )

        variants.append(threshold)

        # ------------------------------------------------
        # Variant 4
        # Sharpen
        # ------------------------------------------------

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

        variants.append(sharp)

        return variants