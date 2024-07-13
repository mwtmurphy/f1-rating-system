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

    dri_df = pd.read_csv(CONFIG["data"]["2024_path"])
    col_df = pd.read_csv(CONFIG["data"]["colour_path"])

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return dri_df, one_off_dict, col_df

dri_df, one_off_dict, col_df = load_data()
curr_df = dri_df.loc[dri_df["round"] == dri_df["round"].max(), ["constructorId", "driverName", "driverScore"]].sort_values("driverScore", ascending=False).reset_index(drop=True)
curr_df = curr_df.merge(col_df, how="left", on="constructorId")

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown("# Current driver ratings")

chart = at.Chart(curr_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("driverScore", title="Driver rating"),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("driverScore:Q", format=".0f", title="Driver score")
    ]
).properties(height=800)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color="black", align="left", dx=2).encode(
    text=at.Text("driverScore:Q", format=".0f")
)

st.altair_chart(bars + text, use_container_width=True)
