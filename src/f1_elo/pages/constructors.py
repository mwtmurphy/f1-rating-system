import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme


# load current constructor data
st.set_page_config(layout="wide")
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)

# data import
@st.cache_data
def load_data() -> tuple:
    '''Returns data for current driver plots'''

    con_df = pd.read_csv(CONFIG["data"]["2024_path"])
    col_df = pd.read_csv(CONFIG["data"]["colour_path"])

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return con_df, one_off_dict, col_df

theme = streamlit_theme.st_theme()
con_df, one_off_dict, col_df = load_data()
curr_df = con_df.loc[con_df["round"] == con_df["round"].max(), ["constructorId", "constructorName", "constructorScore"]].drop_duplicates().sort_values("constructorScore", ascending=False).reset_index(drop=True)
curr_df = curr_df.merge(col_df, how="left", on="constructorId")

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown(f"# {curr_df.loc[0, 'constructorName']} is the current top-rated constructor")

chart = at.Chart(curr_df).encode(
    y=at.Y("constructorName", sort=None, title="Constructor name"),
    x=at.X("constructorScore", stack=None, title="Constructor rating", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("constructorName", title="Constructor name"),
        at.Tooltip("constructorScore:Q", format=".0f", title="Constructor score")
    ]
).properties(height=450)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("constructorScore:Q", format=".0f")
)

st.altair_chart(bars + text, use_container_width=True)

# create most improved constructor vis
agg_df = con_df[["constructorId", "constructorName", "conScoreChange"]].drop_duplicates().groupby(["constructorId", "constructorName"])["conScoreChange"].sum().reset_index()
agg_df = agg_df.merge(col_df, how="left", on="constructorId").sort_values("conScoreChange", ascending=False).reset_index(drop=True)
agg_df["baseline"] = 0

st.markdown(f"# {agg_df.loc[0, 'constructorName']} is the most improved constructor in 2024")

chart = at.Chart(agg_df).encode(
    y=at.Y("constructorName", sort=None, title="Constructor name"),
    x=at.X("conScoreChange", stack=None, title="Constructor rating change", scale=at.Scale(zero=False)),
    x2="baseline",
    tooltip=[
        at.Tooltip("constructorName", title="Constructor name"),
        at.Tooltip("conScoreChange:Q", format=".0f", title="Constructor rating change")
    ]
).properties(height=450)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color=theme["textColor"], align="center", dx=at.expr(at.expr.if_(at.datum.conScoreChange >= 0, 10, -13))).encode(
    text=at.Text("conScoreChange:Q", format=".0f"),
)

st.altair_chart(bars + text, use_container_width=True)