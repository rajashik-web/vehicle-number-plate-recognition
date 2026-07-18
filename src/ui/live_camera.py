import cv2
import streamlit as st

from src.camera import Camera
from src.pipeline import ANPRPipeline
from src.services.anpr_controller import ANPRController
from src.services.parking_manager import ParkingManager
from src.image_storage import ImageStorage


def show_live_camera():

    st.header("🎥 Live ANPR Camera")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Start Camera"):
            st.session_state.camera_running = True

    with col2:
        if st.button("⏹ Stop Camera"):
            st.session_state.camera_running = False

    frame_placeholder = st.empty()

    status_placeholder = st.empty()

    if not st.session_state.camera_running:
        return

    camera = Camera()
    pipeline = ANPRPipeline()

    controller = ANPRController()

    parking = ParkingManager()

    storage = ImageStorage()

    collecting = False

    missing_frames = 0

    MAX_MISSING = 15

    while st.session_state.camera_running:

        frame = camera.read()

        if frame is None:
            break

        result, plates = pipeline.process(frame)

        output = result.plot()

        valid_plate_found = False

        for plate in plates:

            x1, y1, x2, y2 = plate["bbox"]

            text = plate["text"]

            det_conf = plate["confidence"]

            ocr_conf = plate["ocr_confidence"]

            if text != "":

                valid_plate_found = True

                if not collecting:

                    collecting = True

                    controller.start()

                controller.add_plate(
                    text,
                    plate["image"]
                )

                label = (
                    f"{text} "
                    f"OCR:{ocr_conf:.2f} "
                    f"DET:{det_conf:.2f}"
                )

            else:

                label = (
                    f"Unknown "
                    f"OCR:{ocr_conf:.2f}"
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

        if valid_plate_found:

            missing_frames = 0

        else:

            if collecting:
                missing_frames += 1

        if collecting and missing_frames > MAX_MISSING:

            best_plate, best_image = controller.finish()

            if best_plate:

                image_path = storage.save(
                    best_plate,
                    best_image
                )

                success, message = parking.process_vehicle(
                    best_plate,
                    image_path
                )

                if success:
                    status_placeholder.success(message)
                else:
                    status_placeholder.error(message)

            collecting = False

            missing_frames = 0

        rgb = cv2.cvtColor(
            output,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            rgb,
            channels="RGB",
            use_container_width=True
        )

    camera.release()