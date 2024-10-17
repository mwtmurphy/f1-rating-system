import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme


# page config
st.set_page_config(page_title="F1 rating system | Current constructors", layout="wide")
theme = streamlit_theme.st_theme()
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


# helper functions
@st.cache_data
def load_data() -> tuple:
    '''Load and cache data for plots on page'''

    cur_con_df = pd.read_csv(CONFIG["data"]["cur_con_path"])
    con_imp_df = pd.read_csv(CONFIG["data"]["con_imp_path"])

    with open(CONFIG["data"]["last_race_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return cur_con_df, con_imp_df, last_race_dict


# streamlit page
cur_con_df, con_imp_df, last_race_dict = load_data()
st.info(f"Results as of: {last_race_dict['last_race']}")

# plot current constructor ratings
st.markdown(f"# {cur_con_df.loc[0, 'constructorName']} is the current top-rated constructor")

chart = at.Chart(cur_con_df).encode(
    y=at.Y("constructorName", sort=None, title="Constructor"),
    x=at.X("constructorScore", stack=None, title="Rating", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("constructorName", title="Constructor"),
        at.Tooltip("constructorScore:Q", format=".0f", title="Rating")
    ]
).properties(height=450)
bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)
text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("constructorScore:Q", format=".0f")
)
st.altair_chart(bars + text, use_container_width=True)

# plot rating changes for current constructors
st.markdown(f"# {con_imp_df.loc[0, 'constructorName']} is the most improved constructor in 2024")

chart = at.Chart(con_imp_df).encode(
    y=at.Y("constructorName", sort=None, title="Constructor"),
    x=at.X("conScoreChange", stack=None, title="Rating change", scale=at.Scale(zero=False)),
    x2="baseline",
    tooltip=[
        at.Tooltip("constructorName", title="Constructor"),
        at.Tooltip("conScoreChange:Q", format=".0f", title="Rating change")
    ]
).properties(height=450)
bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)
text = chart.mark_text(
    color=theme["textColor"], 
    align=at.expr(at.expr.if_(at.datum.conScoreChange >= 0, "left", "right")), 
    dx=at.expr(at.expr.if_(at.datum.conScoreChange >= 0, 2, -2))
).encode(
    text=at.Text("conScoreChange:Q", format=".0f"),
)
st.altair_chart(bars + text, use_container_width=True)
