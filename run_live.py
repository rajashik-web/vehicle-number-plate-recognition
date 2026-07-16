import cv2

from src.camera import Camera
from src.pipeline import ANPRPipeline
from src.services.anpr_controller import ANPRController
from src.services.parking_manager import ParkingManager
from src.config import MAX_MISSING_FRAMES


camera = Camera()
pipeline = ANPRPipeline()

controller = ANPRController()
parking = ParkingManager()

collecting = False
missing_frames = 0


while True:

    frame = camera.read()

    if frame is None:
        break

    # ----------------------------------
    # Run ANPR Pipeline
    # ----------------------------------

    result, plates = pipeline.process(frame)

    output = result.plot()

    valid_plate_found = False

    # ----------------------------------
    # Process OCR Results
    # ----------------------------------

    for plate in plates:

        x1, y1, x2, y2 = plate["bbox"]

        plate_text = plate["text"]

        ocr_conf = plate["ocr_confidence"]

        det_conf = plate["confidence"]

        # -------------------------
        # Valid Plate
        # -------------------------

        if plate_text:

            valid_plate_found = True

            if not collecting:

                collecting = True
                controller.start()

                print("\n==============================")
                print("Started OCR Session")
                print("==============================")

            controller.add_plate(plate_text)

        # -------------------------
        # Display Label
        # -------------------------

        status = plate_text if plate_text else "Unknown"

        label = (
            f"{status} | "
            f"OCR:{ocr_conf:.2f} | "
            f"DET:{det_conf:.2f}"
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

    # ----------------------------------
    # Vehicle Visible
    # ----------------------------------

    if valid_plate_found:

        missing_frames = 0

    elif collecting:

        missing_frames += 1

    # ----------------------------------
    # Vehicle Left Camera
    # ----------------------------------

    if collecting and missing_frames > MAX_MISSING_FRAMES:

        print("\n==============================")
        print("Vehicle Left Camera")
        print("==============================")

        best_plate = controller.finish()

        print("Best Plate :", best_plate)

        if best_plate:

            success, message = parking.process_vehicle(
    best_plate
)
            print(message)

        collecting = False
        missing_frames = 0

    # ----------------------------------
    # Display
    # ----------------------------------

    cv2.imshow(
        "Live ANPR",
        output
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


camera.release()

cv2.destroyAllWindows()