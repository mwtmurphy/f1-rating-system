import plotly.express as px
import streamlit as st

# app config
goat_page = st.Page("pages/goat.py", title="Who is the F1 Goat?", url_path="who-is-the-goat", icon=":material/star:")
cur_dri_page = st.Page("pages/current_drivers.py", title="Current driver ratings", url_path="current-driver-ratings", icon=":material/sports_motorsports:")
cur_con_page = st.Page("pages/current_constructors.py", title="Current constructor ratings", url_path="current-constructor-ratings", icon=":material/auto_transmission:")
com_dri_page = st.Page("pages/compare_drivers.py", title="Compare driver ratings", url_path="compare-driver-ratings", icon=":material/group:")
com_con_page = st.Page("pages/compare_constructors.py", title="Compare constructor ratings", url_path="compare-constructor-ratings", icon=":material/swap_driving_apps:")

page_nav = st.navigation([goat_page, cur_dri_page, cur_con_page, com_dri_page, com_con_page])
page_nav.run()

st.sidebar.markdown("""
    Created by Mitchell Murphy, Data Scientist using data to improve
    decision-making. 
    
    Code for this project can be found
    [here](https://github.com/mwtmurphy/f1-rating-system). Data for 
    this project is sourced from the [Ergast API](http://ergast.com/mrd).
                    
    If you like this project, see my other work on 
    [Github](https://github.com/mwtmurphy) or connect with me on 
    [LinkedIn](https://www.linkedin.com/in/mwtmurphy).
""")
