import json
import yaml

import altair as at
import pandas as pd
import streamlit as st


# load current driver data
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

con_df, one_off_dict, col_df = load_data()
curr_df = con_df.loc[con_df["round"] == con_df["round"].max(), ["constructorId", "constructorName", "constructorScore"]].drop_duplicates().sort_values("constructorScore", ascending=False).reset_index(drop=True)
curr_df = curr_df.merge(col_df, how="left", on="constructorId")

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown("# Current constructor ratings")

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

text = chart.mark_text(color="black", align="left", dx=2).encode(
    text=at.Text("constructorScore:Q", format=".0f")
)

st.altair_chart(bars + text, use_container_width=True)
