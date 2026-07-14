import os
import cv2
from datetime import datetime


class ImageStorage:

    def __init__(self):

        self.output_dir = "data/vehicles"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def save(self, plate_number, image):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"{plate_number}_{timestamp}.jpg"
        )

        path = os.path.join(
            self.output_dir,
            filename
        )

        cv2.imwrite(path, image)

        return path