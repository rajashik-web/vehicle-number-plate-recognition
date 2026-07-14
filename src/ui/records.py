import streamlit as st
import pandas as pd


def show_records(records):

    st.header("🅿️ Parking Records")

    if len(records) == 0:

        st.info("No parking records found.")

        return

    df = pd.DataFrame(
        records,
        columns=[
            "Plate Number",
            "Entry Time",
            "Exit Time",
            "Status",
            "Parking Fee (₹)"
        ]
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.divider()