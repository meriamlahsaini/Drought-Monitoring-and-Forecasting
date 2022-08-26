import streamlit as st
from multiapp import MultiApp
from apps import home, Drought_Monitoring, Drought_Forecasting

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Drought Monitoring", Drought_Monitoring.app)
apps.add_app("Drought Forecasting", Drought_Forecasting.app)
# apps.add_app("Change opacity", opacity.app)
# apps.add_app("Search datasets", datasets.app)
# apps.add_app("NLCD Demo", nlcd_demo.app)

# The main app
apps.run()
