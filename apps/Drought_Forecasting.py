import streamlit as st


def app():
    st.title("Drought Forecasting")

    countries = (
        "Zambia",
        "Ethiopia"
    )

    country = st.selectbox("Country", countries)
   


    st.header("Example")
