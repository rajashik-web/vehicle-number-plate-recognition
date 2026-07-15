import cv2

from src.preprocessing import PlatePreprocessor

image = cv2.imread(
    "data/output/plate_0.jpg"
)

preprocessor = PlatePreprocessor()

processed = preprocessor.process(
    image
)

cv2.imshow(
    "Original",
    image
)

cv2.imshow(
    "Processed",
    processed
)

cv2.waitKey(0)

cv2.destroyAllWindows()