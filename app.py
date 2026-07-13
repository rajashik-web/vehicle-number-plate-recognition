import streamlit as st
from PIL import Image
import cv2
import numpy as np

from src.pipeline import ANPRPipeline

# -----------------------------------
# Streamlit Configuration
# -----------------------------------

st.set_page_config(
    page_title="Vehicle Number Plate Recognition",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Vehicle Number Plate Recognition")

st.write(
    "Upload a vehicle image to detect license plates."
)

# -----------------------------------
# Load Pipeline
# -----------------------------------

@st.cache_resource
def load_pipeline():
    return ANPRPipeline()


pipeline = load_pipeline()

# -----------------------------------
# Upload Image
# -----------------------------------

uploaded_file = st.file_uploader(
    "Choose a vehicle image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# Process Image
# -----------------------------------

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)

    # Convert PIL -> OpenCV
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Run Pipeline
    result, plates = pipeline.process(image_cv)

    # Draw bounding boxes
    annotated_image = result.plot()
    annotated_image = cv2.cvtColor(
        annotated_image,
        cv2.COLOR_BGR2RGB
    )

    # -----------------------------------
    # Show Images
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📤 Uploaded Image")

        st.image(
            image,
            width="stretch"
        )

    with col2:

        st.subheader("🎯 Detection Result")

        st.image(
            annotated_image,
            width="stretch"
        )

    # -----------------------------------
    # Summary
    # -----------------------------------

    st.divider()

    st.success(
        f"Detected {len(plates)} license plate(s)"
    )

    st.metric(
        "License Plates Detected",
        len(plates)
    )

    # -----------------------------------
    # Display Plates
    # -----------------------------------

    st.divider()

    st.subheader("🚘 Detected Plates")

    if len(plates) == 0:

        st.warning("No license plate detected.")

    else:

        for index, plate in enumerate(plates):

            st.markdown(f"### Plate {index + 1}")

            plate_rgb = cv2.cvtColor(
                plate["image"],
                cv2.COLOR_BGR2RGB
            )

            st.image(
                plate_rgb,
                width=300
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Confidence",
                    f"{plate['confidence'] * 100:.2f}%"
                )

            with col2:

                st.code(
                    f"Bounding Box: {plate['bbox']}"
                )

            st.divider()