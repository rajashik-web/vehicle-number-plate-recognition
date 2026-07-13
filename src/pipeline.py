from src.detector import PlateDetector
from src.ocr import OCRReader


class ANPRPipeline:

    def __init__(self):

        self.detector = PlateDetector()
        self.ocr = OCRReader()

    def process(self, image):

        # Run YOLO
        result = self.detector.detect(image)

        # Extract cropped plates
        plates = self.detector.extract_plates(
            image,
            result
        )

        # OCR placeholder
        for plate in plates:

            ocr_result = self.ocr.read_text(
                plate["image"]
            )

            plate["text"] = ocr_result["text"]
            plate["ocr_confidence"] = ocr_result["confidence"]

        return result, plates