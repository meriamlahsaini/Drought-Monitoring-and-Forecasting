import streamlit as st
from multiapp import MultiApp
from apps import Introduction, Drought_Monitoring, Drought_Forecasting

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Introduction", Introduction.app)
apps.add_app("Drought Monitoring", Drought_Monitoring.app)
apps.add_app("Drought Forecasting", Drought_Forecasting.app)


# The main app
apps.run()
