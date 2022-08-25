import streamlit as st
from multiapp import MultiApp
from apps import home, Drought_Monitoring
from dataset import *
from args import get_main_args

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Drought Monitoring", Drought_Monitoring.app)
# apps.add_app("Change basemaps", basemaps.app)
# apps.add_app("Change opacity", opacity.app)
# apps.add_app("Search datasets", datasets.app)
# apps.add_app("NLCD Demo", nlcd_demo.app)

# The main app
apps.run()
