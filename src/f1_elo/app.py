import plotly.express as px
import streamlit as st

# app config
goat_page = st.Page("pages/goat.py", title="Who is the F1 Goat?", url_path="the-goat", icon=":material/star:")
dri_page = st.Page("pages/drivers.py", title="Current driver ratings", url_path="driver-ratings", icon=":material/sports_motorsports:")
con_page = st.Page("pages/constructors.py", title="Current constructor ratings", url_path="constructor-ratings", icon=":material/auto_transmission:")

page_nav = st.navigation([goat_page, dri_page, con_page])
page_nav.run()
