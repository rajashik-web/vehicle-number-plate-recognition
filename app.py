import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd

from src.pipeline import ANPRPipeline
from src.database import DatabaseManager
from src.image_storage import ImageStorage

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


@st.cache_resource
def load_database():
    return DatabaseManager()


pipeline = load_pipeline()
db = load_database()
storage = ImageStorage()

# -----------------------------------
# Upload Image
# -----------------------------------

uploaded_file = st.file_uploader("Choose a vehicle image", type=["jpg", "jpeg", "png"])

# -----------------------------------
# Process Image
# -----------------------------------

if uploaded_file is not None:

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

                        image_path = storage.save(plate_number.upper(), image_cv)

                        success = db.add_vehicle(plate_number.upper(), image_path)

                        if success:

                            st.success(f"{plate_number.upper()} entered successfully.")

                        else:

                            st.warning(f"{plate_number.upper()} is already inside.")

            with col2:

                if st.button("🚙 Vehicle Exit", key=f"exit_{index}"):

                    if plate_number.strip() == "":

                        st.error("Please enter the vehicle number.")

                    else:

                        success = db.vehicle_exit(plate_number.upper())

                        if success:

                            st.success(f"{plate_number.upper()} exited successfully.")

                        else:

                            st.error("Vehicle not found.")

            st.divider()

# -----------------------------------
# Dashboard Statistics
# -----------------------------------

stats = db.get_dashboard_stats()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🚗 Vehicles Inside", stats["inside"])

with col2:
    st.metric("🚙 Total Vehicles", stats["total"])

with col3:
    st.metric("💰 Total Revenue", f"₹{stats['revenue']}")

st.divider()

# -----------------------------------
# Parking Records Dashboard
# -----------------------------------

st.header("🅿️ Parking Records")

records = db.get_all_records()

if len(records) == 0:

    st.info("No parking records found.")

else:

    df = pd.DataFrame(
        records,
        columns=[
            "Plate Number",
            "Entry Time",
            "Exit Time",
            "Status",
            "Parking Fee (₹)",
        ],
    )

    # -----------------------------------
    # Search Vehicle
    # -----------------------------------

    st.divider()

    st.header("🔍 Search Vehicle")

    search_plate = st.text_input("Enter Vehicle Number")

    if st.button("Search"):

        if search_plate.strip() == "":

            st.warning("Please enter a vehicle number.")

        else:

            record = db.search_vehicle(search_plate.upper())

            if record is None:

                st.error("Vehicle not found.")

            else:

                st.success("Vehicle Found")

                st.write(f"**Plate Number:** {record[0]}")
                st.write(f"**Entry Time:** {record[1]}")
                st.write(f"**Exit Time:** {record[2]}")
                st.write(f"**Status:** {record[3]}")
                st.write(f"**Parking Fee:** ₹{record[4]}")
