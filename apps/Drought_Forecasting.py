import streamlit as st


def app():
    st.title("Drought Forecasting")

    countries = (
        "Afghanistan",
        "Burkina Faso",
        "Ethiopia",
        "Ghana",
        "Kenya",
        "Senegal",
        "Zambia"
    )

    country = st.selectbox("Country", countries)
    
    study_years = st.slider("Study Years", 2012, 2022, 2012)
    study_months_gs = st.slider("Study Months", 1, 4, 1)   # growing season
    study_months_ss = st.slider("Study Months", 11, 12, 11)   # sowing season
   


    st.header("Example")
