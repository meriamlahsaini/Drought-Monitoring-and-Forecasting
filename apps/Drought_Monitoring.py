import streamlit as st




def show_drought_monitor_page():
    st.title("Drought Forecasting")

    countries = (
        "Zambia",
        "Ethiopia"
    )

    country = st.selectbox("Country", countries)
