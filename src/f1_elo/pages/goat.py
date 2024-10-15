import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme


# page config
st.set_page_config(layout="wide")
theme = streamlit_theme.st_theme()
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


# helper functions
@st.cache_data
def load_data() -> tuple:
    '''Load and cache data for plots on page'''

    avg_goat_df = pd.read_csv(CONFIG["data"]["avg_goat_path"])
    avg_hist_df = pd.read_csv(CONFIG["data"]["avg_hist_path"])

    with open(CONFIG["data"]["last_race_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return avg_goat_df, avg_hist_df, last_race_dict


# streamlit page
avg_goat_df, avg_hist_df, last_race_dict = load_data()
st.info(f"Results as of: {last_race_dict['last_race']}")

# plot top 10 drivers based on mean career rating 
st.markdown(f"# {avg_goat_df.loc[0, 'driverName']} is the rating GOAT")
st.markdown("Based on a driver's mean rating for all races started.")

chart = at.Chart(avg_goat_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("meanScore", stack=None, title="Mean driver rating", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("meanScore:Q", format=".0f", title="Mean driver score")
    ]
).properties(height=450)
bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)
text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("meanScore:Q", format=".0f")
)
st.altair_chart(bars + text, use_container_width=True)

# plot driver ratings for top 3 drivers over time
order = avg_goat_df.loc[:2, "driverName"].to_list()

scale = at.Scale(domain=order, range=["#FFD700", "#C0C0C0", "#CD7F32"])
chart = at.Chart(avg_hist_df).encode(
    x=at.X("date", title="Date"),
    y=at.Y("driverScore", title="Driver rating", scale=at.Scale(zero=False)),
    color=at.Color("driverName", title="Driver name", sort=order, scale=scale),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("driverScore:Q", format=".0f", title="Driver rating")
    ]
)
lines = chart.mark_line()
st.altair_chart(lines, use_container_width=True)
