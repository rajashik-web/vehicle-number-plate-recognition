import streamlit as st
import cv2

from src.camera import Camera


def show_live_camera():

    st.header("🎥 Live Camera")

    start = st.button("▶ Start Camera")

    stop = st.button("⏹ Stop")

    frame_placeholder = st.empty()

    if start:

        camera = Camera()

        while True:

            frame = camera.read()

            if frame is None:
                break

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame_placeholder.image(
                frame,
                channels="RGB",
                use_container_width=True
            )

            if stop:
                break

        camera.release()