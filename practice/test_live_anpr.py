import cv2

from src.camera import Camera
from src.pipeline import ANPRPipeline

camera = Camera()
pipeline = ANPRPipeline()

while True:

    frame = camera.read()

    if frame is None:
        break

    # Run ANPR pipeline
    result, plates = pipeline.process(frame)

    # Draw YOLO detections
    output = result.plot()

    # Display OCR result
    for plate in plates:

        x1, y1, x2, y2 = plate["bbox"]

        plate_text = plate["text"]
        ocr_conf = plate["ocr_confidence"]
        det_conf = plate["confidence"]

        if plate_text != "":

            label = (
                f"{plate_text} | "
                f"OCR: {ocr_conf:.2f} | "
                f"DET: {det_conf:.2f}"
            )

        else:

            label = (
                f"Unknown | "
                f"OCR: {ocr_conf:.2f} | "
                f"DET: {det_conf:.2f}"
            )

        cv2.putText(
            output,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Live ANPR",
        output
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()