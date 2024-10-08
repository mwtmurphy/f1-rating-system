import plotly.express as px
import streamlit as st
import st_social_media_links

# app config
goat_page = st.Page("pages/goat.py", title="Who is the F1 Goat?", url_path="the-goat", icon=":material/star:")
dri_page = st.Page("pages/drivers.py", title="Current driver ratings", url_path="driver-ratings", icon=":material/sports_motorsports:")
con_page = st.Page("pages/constructors.py", title="Current constructor ratings", url_path="constructor-ratings", icon=":material/auto_transmission:")

page_nav = st.navigation([goat_page, dri_page, con_page])
page_nav.run()

st.sidebar.markdown("""
    Created by Mitchell Murphy, Lead Data Scientist with over 8 years of experience. See the code 
    for this project [here](https://github.com/mwtmurphy/f1-rating-system).
                    
    If you like this project, see my other projects or send me a message via the links below:
""")
social_icons = st_social_media_links.SocialMediaIcons([
    "https://mwtmurphy.github.io/portfolio/",
    "https://github.com/mwtmurphy",
    "https://www.linkedin.com/in/mwtmurphy/"
])
social_icons.render(sidebar=True)