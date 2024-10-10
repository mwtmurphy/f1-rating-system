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
    hist_df = pd.read_csv(CONFIG["data"]["hist_path"])

    # create driver improvement data
    imp_df = dri_df.copy()
    imp_df["cumDriScoreChange"] = imp_df.groupby("driverId")["driScoreChange"].cumsum()
    imp_df = imp_df.sort_values("round").drop_duplicates("driverId", keep="last")[["constructorId", "driverName", "cumDriScoreChange"]]
    imp_df = imp_df.merge(col_df, how="left", on="constructorId").sort_values("cumDriScoreChange", ascending=False)
    imp_df = imp_df.reset_index(drop=True).drop(columns="constructorId")
    imp_df["baseline"] = 0

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return dri_df, one_off_dict, col_df, hist_df, imp_df

theme = streamlit_theme.st_theme()
dri_df, one_off_dict, col_df, hist_df, imp_df = load_data()
curr_df = dri_df.loc[dri_df["round"] == dri_df["round"].max(), ["constructorId", "driverName", "driverScore"]].sort_values("driverScore", ascending=False).reset_index(drop=True)
curr_df = curr_df.merge(col_df, how="left", on="constructorId")

# create current top-rated driver vis
st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown(f"# {curr_df.loc[0, 'driverName']} is the current top-rated driver")

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

# create most improved driver vis
st.markdown(f"# {imp_df.loc[0, 'driverName']} is the most improved driver in 2024")

chart = at.Chart(imp_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("cumDriScoreChange", stack=None, title="Driver rating change", scale=at.Scale(zero=False)),
    x2="baseline",
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("cumDriScoreChange:Q", format=".0f", title="Driver rating change")
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

# plot chosen driver scores over 2024
st.title("Compare your favourite drivers")
selected_drivers = st.multiselect(label="Select drivers to compare.", options=sorted(list(set(hist_df["driverName"]))), default=["Max Verstappen", "Lando Norris"])
sd_sub_df = hist_df[hist_df["driverName"].isin(selected_drivers)]

line_chart = at.Chart(sd_sub_df).mark_line().encode(
    x=at.X("date", stack=None, title="Date"),
    y=at.Y("driverScore", sort=None, title="Driver score", scale=at.Scale(zero=False)),
    color=at.Text("driverName", title="Driver name"),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("driverScore:Q", format=".0f", title="Driver score")
    ]
)

st.altair_chart(line_chart, use_container_width=True)
