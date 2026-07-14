import streamlit as st


def show_dashboard(stats):

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚗 Vehicles Inside",
            stats["inside"]
        )

    with col2:
        st.metric(
            "🚙 Total Vehicles",
            stats["total"]
        )

    with col3:
        st.metric(
            "💰 Total Revenue",
            f"₹{stats['revenue']}"
        )

    st.divider()