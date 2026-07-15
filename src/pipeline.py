from src.detector import PlateDetector
from src.ocr import OCRReader
from src.utils import normalize_plate, is_valid_plate
from src.validator import PlateValidator
from src.corrector import PlateCorrector


class ANPRPipeline:

    def __init__(self):

        self.detector = PlateDetector()
        self.ocr = OCRReader()
        self.validator = PlateValidator()
        self.corrector = PlateCorrector()

    def process(self, image):

        # Run YOLO
        result = self.detector.detect(image)

        # Extract cropped plates
        plates = self.detector.extract_plates(
            image,
            result
        )

        # OCR
        for plate in plates:

            ocr_result = self.ocr.read_text(
                plate["image"]
            )

            text = normalize_plate(
    ocr_result["text"]
)

            text = self.corrector.correct(
                text
            )

            print("OCR Raw:", ocr_result["text"])
            print("Normalized:", text)
            print("Valid:", self.validator.is_valid(text))

            if self.validator.is_valid(text):
                plate["text"] = text
            else:
                plate["text"] = ""

            plate["ocr_confidence"] = ocr_result["confidence"]

        return result, plates