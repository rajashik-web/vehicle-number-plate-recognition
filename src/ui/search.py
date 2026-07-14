import streamlit as st


def show_search(parking):

    st.header("🔍 Search Vehicle")

    search_plate = st.text_input(
        "Enter Vehicle Number"
    )

    if st.button("Search"):

        if search_plate.strip() == "":

            st.warning(
                "Please enter a vehicle number."
            )

            return

        record = parking.search(
            search_plate.upper()
        )

        if record is None:

            st.error(
                "Vehicle not found."
            )

            return

        st.success("Vehicle Found")

        st.write(
            f"**Plate Number:** {record[0]}"
        )

        st.write(
            f"**Entry Time:** {record[1]}"
        )

        st.write(
            f"**Exit Time:** {record[2]}"
        )

        st.write(
            f"**Status:** {record[3]}"
        )

        st.write(
            f"**Parking Fee:** ₹{record[4]}"
        )