import cv2
import numpy as np


class PlatePreprocessor:

    def process(self, image):

        # Resize
        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        # Grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # Remove noise while preserving edges
        gray = cv2.bilateralFilter(
            gray,
            11,
            17,
            17
        )

        # Improve contrast
        gray = cv2.equalizeHist(
            gray
        )

        # Sharpen
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

        return sharp