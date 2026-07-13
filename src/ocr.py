class OCRReader:
    """
    OCR interface.

    This class will later use PaddleOCR to read
    license plate text.
    """

    def __init__(self):
        pass

    def read_text(self, image):
        """
        Placeholder implementation.

        Args:
            image: Cropped license plate image.

        Returns:
            dict
        """

        return {
            "text": "",
            "confidence": 0.0
        }