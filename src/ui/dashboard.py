import streamlit as st
import pandas as pd


def show_dashboard(stats):

    st.header("📊 Smart Parking Dashboard")

    inside = stats.get("inside", 0)
    total = stats.get("total", 0)
    revenue = stats.get("revenue", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚗 Vehicles Inside",
            inside
        )

    with col2:
        st.metric(
            "🚙 Total Vehicles",
            total
        )

    with col3:
        st.metric(
            "💰 Total Revenue",
            f"₹{revenue:.2f}"
        )

    st.divider()

    # ----------------------------------------
    # Parking Occupancy
    # ----------------------------------------

    st.subheader("🚘 Parking Occupancy")

    if total > 0:

        occupancy = (inside / total) * 100

    else:

        occupancy = 0

    st.progress(min(int(occupancy), 100))

    st.caption(f"{occupancy:.1f}% Occupancy")

    st.divider()

    # ----------------------------------------
    # Quick Summary
    # ----------------------------------------

    summary = pd.DataFrame(
        {
            "Metric": [
                "Vehicles Inside",
                "Vehicles Processed",
                "Revenue"
            ],
            "Value": [
                inside,
                total,
                f"₹{revenue:.2f}"
            ]
        }
    )

    st.subheader("📋 Summary")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )