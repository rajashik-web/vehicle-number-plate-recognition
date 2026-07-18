import os
import streamlit as st


def show_search(parking):

    st.header("🔍 Search Vehicle")

    search_plate = st.text_input(
        "Enter Vehicle Number"
    ).strip().upper()

    if st.button("Search"):

        if search_plate == "":

            st.warning(
                "Please enter a vehicle number."
            )

            return

        record = parking.search(search_plate)

        if record is None:

            st.error(
                "Vehicle not found."
            )

            return

        plate = record[0]
        entry_time = record[1]
        exit_time = record[2]
        status = record[3]
        parking_fee = record[4]
        image_path = record[5]

        st.success("Vehicle Found")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Vehicle Number",
                plate
            )

            st.metric(
                "Status",
                status
            )

            st.metric(
                "Parking Fee",
                f"₹{parking_fee:.2f}"
            )

        with col2:

            st.write(
                f"**Entry Time:** {entry_time}"
            )

            st.write(
                f"**Exit Time:** {exit_time if exit_time else '-'}"
            )

        st.divider()

        st.subheader("Vehicle Image")

        if image_path and os.path.exists(image_path):

            st.image(
                image_path,
                caption=plate,
                use_container_width=True
            )

        else:

            st.info("No vehicle image available.")