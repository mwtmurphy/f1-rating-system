import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme

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

theme = streamlit_theme.st_theme()
dri_df, one_off_dict, col_df = load_data()
curr_df = dri_df.loc[dri_df["round"] == dri_df["round"].max(), ["constructorId", "driverName", "driverScore"]].sort_values("driverScore", ascending=False).reset_index(drop=True)
curr_df = curr_df.merge(col_df, how="left", on="constructorId")

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown("# Current driver ratings")

chart = at.Chart(curr_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("driverScore", stack=None, title="Driver rating", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("driverScore:Q", format=".0f", title="Driver score")
    ]
).properties(height=800)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("driverScore:Q", format=".0f")
)

st.altair_chart(bars + text, use_container_width=True)

# st.markdown("# Driver performance")

# agg_df = dri_df.groupby(["constructorId", "driverId", "driverName"])["outperformance"].sum().reset_index()
# agg_df = agg_df.merge(col_df, how="left", on="constructorId").sort_values("outperformance", ascending=False)
# agg_df["baseline"] = 0

# chart = at.Chart(agg_df).encode(
#     y=at.Y("driverName", sort=None, title="Driver name"),
#     x=at.X("outperformance", stack=None, title="Driver outperformance", scale=at.Scale(zero=False)),
#     x2="baseline",
#     tooltip=[
#         at.Tooltip("driverName", title="Driver name"),
#         at.Tooltip("outperformance:Q", format=".2f", title="Driver outperformance")
#     ]
# ).properties(height=800)

# bars = chart.mark_bar(size=30).encode(
#     color=at.Color("hex_code:N", scale=None)
# )

# align_condition = at.condition("datum.outperformance > 0", at.value('left'), at.value('right'))
# dx_condition = at.condition("datum.outperformance > 0", at.value(2), at.value(-2))
# text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
#     text=at.Text("outperformance:Q", format=".2f"), 
#     #dx=dx_condition
# )

# st.altair_chart(bars + text, use_container_width=True)
