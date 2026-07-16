import streamlit as st
from PIL import Image
import cv2
import numpy as np

from src.pipeline import ANPRPipeline
from src.services.parking_manager import ParkingManager
from src.ui.dashboard import show_dashboard
from src.ui.records import show_records
from src.ui.live_camera import show_live_camera
from src.image_storage import ImageStorage
from src.ui.search import show_search

# -----------------------------------
# Streamlit Configuration
# -----------------------------------

st.set_page_config(
    page_title="Vehicle Number Plate Recognition", page_icon="🚗", layout="wide"
)

st.title("🚗 AI Smart Parking Management System")

st.write("Upload a vehicle image to detect license plates and register vehicle entry.")

# -----------------------------------
# Load Resources
# -----------------------------------


@st.cache_resource
def load_pipeline():
    return ANPRPipeline()


pipeline = load_pipeline()
parking = ParkingManager()
storage = ImageStorage()

# -----------------------------------
# Sidebar Navigation
# -----------------------------------

page = st.sidebar.radio(
    "📋 Navigation",
    [
        "Upload Image",
        "🎥 Live Camera",
        "📊 Dashboard",
        "📋 Records",
        "🔍 Search"
    ]
)

# -----------------------------------
# Upload Image
# -----------------------------------

if page == "Upload Image":

    uploaded_file = st.file_uploader(
        "Choose a vehicle image",
        type=["jpg", "jpeg", "png"]
    )

else:

    uploaded_file = None

# -----------------------------------
# Process Image
# -----------------------------------

if page == "Upload Image" and uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)

    # Convert PIL -> OpenCV
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Run detection pipeline
    result, plates = pipeline.process(image_cv)

    # Draw detection boxes
    annotated_image = result.plot()
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    # -----------------------------------
    # Display Images
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📤 Uploaded Image")

        st.image(image, width="stretch")

    with col2:

        st.subheader("🎯 Detection Result")

        st.image(annotated_image, width="stretch")

    # -----------------------------------
    # Summary
    # -----------------------------------

    st.divider()

    st.success(f"Detected {len(plates)} license plate(s)")

    st.metric("License Plates Detected", len(plates))

    # -----------------------------------
    # Display Plates
    # -----------------------------------

    st.divider()

    st.subheader("🚘 Detected Plates")

    if len(plates) == 0:

        st.warning("No license plate detected.")

    else:

        for index, plate in enumerate(plates):

            st.markdown(f"## Plate {index + 1}")

            plate_rgb = cv2.cvtColor(plate["image"], cv2.COLOR_BGR2RGB)

            st.image(plate_rgb, width=300)

            st.metric("Detection Confidence", f"{plate['confidence'] * 100:.2f}%")

            st.code(f"Bounding Box: {plate['bbox']}")

            plate_key = f"plate_{index}"

            # Update OCR result whenever a new image is processed
            st.session_state[plate_key] = plate["text"]

            plate_number = st.text_input(f"Plate Number {index + 1}", key=plate_key)

            st.caption(f"OCR Confidence: {plate['ocr_confidence']:.2f}")

            if plate["text"] == "":

                st.warning(
                    "OCR could not confidently recognize the plate. Please enter it manually."
                )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("🚗 Vehicle Entry", key=f"entry_{index}"):

                    if plate_number.strip() == "":

                        st.error("Please enter the vehicle number.")

                    else:

                        image_path = storage.save(plate_number.upper(), plate["image"])

                        success, message = parking.vehicle_entry(
                            plate_number.upper(), image_path
                        )

                        if success:

                            st.success(message)

                        else:

                            st.error(message)

            with col2:

                if st.button("🚙 Vehicle Exit", key=f"exit_{index}"):

                    if plate_number.strip() == "":

                        st.error("Please enter the vehicle number.")

                    else:

                        success, message = parking.vehicle_exit(plate_number.upper())

                        if success:

                            st.success(message)

                        else:

                            st.error(message)

                        if success:

                            st.success(f"{plate_number.upper()} exited successfully.")

                        else:

                            st.error("Vehicle not found.")

            st.divider()
# -----------------------------------
# Other Pages
# -----------------------------------

if page == "📊 Dashboard":

    show_dashboard(
        parking.dashboard()
    )

elif page == "📋 Records":

    show_records(
        parking.records()
    )

elif page == "🔍 Search":

    show_search(
        parking
    )

elif page == "🎥 Live Camera":

    show_live_camera()