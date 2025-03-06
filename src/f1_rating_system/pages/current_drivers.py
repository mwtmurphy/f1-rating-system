import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme


# page config
st.set_page_config(page_title="F1 rating system | Current drivers", layout="wide")
theme = streamlit_theme.st_theme()
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


# helper functions
@st.cache_data
def load_data() -> tuple:
    '''Load and cache data for plots on page'''

    cur_dri_df = pd.read_csv(CONFIG["data"]["cur_dri_path"])
    dri_imp_df = pd.read_csv(CONFIG["data"]["dri_imp_path"])

    with open(CONFIG["data"]["last_race_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return cur_dri_df, dri_imp_df, last_race_dict


# streamlit page 
cur_dri_df, dri_imp_df, last_race_dict = load_data()
st.info(f"Results as of: {last_race_dict['last_race']}")

# plot current driver ratings
st.markdown(f"# {cur_dri_df.loc[0, 'driverName']} is the current top-rated driver")

chart = at.Chart(cur_dri_df).encode(
    y=at.Y("driverName", sort=None, title="Driver"),
    x=at.X("driverScore", stack=None, title="Rating", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("driverName", title="Driver"),
        at.Tooltip("driverScore:Q", format=".0f", title="Rating")
    ]
).properties(height=800)
bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)
text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("driverScore:Q", format=".0f")
)
st.altair_chart(bars + text, use_container_width=True)

# plot rating changes for current drivers
st.markdown(f"# {dri_imp_df.loc[0, 'driverName']} is the most improved driver in 2024")

chart = at.Chart(dri_imp_df).encode(
    y=at.Y("driverName", sort=None, title="Driver"),
    x=at.X("cumDriScoreChange", stack=None, title="Rating change", scale=at.Scale(zero=False)),
    x2="baseline",
    tooltip=[
        at.Tooltip("driverName", title="Driver"),
        at.Tooltip("cumDriScoreChange:Q", format=".0f", title="Rating change")
    ]
).properties(height=800)
bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)
text = chart.mark_text(
    color=theme["textColor"], 
    align=at.expr(at.expr.if_(at.datum.cumDriScoreChange >= 0, "left", "right")), 
    dx=at.expr(at.expr.if_(at.datum.cumDriScoreChange >= 0, 2, -2))
).encode(
    text=at.Text("cumDriScoreChange:Q", format=".0f"),
)
st.altair_chart(bars + text, use_container_width=True)
