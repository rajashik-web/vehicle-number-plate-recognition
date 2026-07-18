import os
import pandas as pd
import streamlit as st


def show_records(records):

    st.header("📋 Parking Records")

    if not records:
        st.info("No parking records found.")
        return

    rows = []

    for record in records:

        plate = record[0]
        entry = record[1]
        exit_time = record[2]
        status = record[3]
        fee = record[4]
        image_path = record[5]

        rows.append({
            "Plate Number": plate,
            "Entry Time": entry,
            "Exit Time": exit_time if exit_time else "-",
            "Status": status,
            "Parking Fee (₹)": float(fee),
            "Image": "Available" if image_path and os.path.exists(image_path) else "Not Available"
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Vehicle Images")

    for record in records:

        plate = record[0]
        image_path = record[5]

        if image_path and os.path.exists(image_path):

            with st.expander(f"🚗 {plate}"):

                st.image(
                    image_path,
                    caption=plate,
                    use_container_width=True
                )