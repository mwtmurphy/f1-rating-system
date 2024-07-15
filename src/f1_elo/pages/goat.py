import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme


# app config
st.set_page_config(layout="wide")
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


# data import
@st.cache_data
def load_data() -> tuple:
    '''Returns dataframe with ELO scores for drivers under GOAT 
    consideration and dataframe with days top ranked'''
    
    goat_df = pd.read_csv(CONFIG["data"]["goat_path"])
    hist_df = pd.read_csv(CONFIG["data"]["hist_path"])

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return goat_df, hist_df, one_off_dict

theme = streamlit_theme.st_theme()
goat_df, hist_df, one_off_dict = load_data()

avg_score_df = goat_df.sort_values("meanScore", ascending=False).head(10).reset_index(drop=True)
avg_score_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_score_df.shape[0] - 3)

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown(f"# {avg_score_df.loc[0, 'driverName']} is the rating GOAT")
st.markdown("For all races started, the driver's mean rating.")

# create mean score bar chart
chart = at.Chart(avg_score_df).encode(
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

# create mean score time series plot
as_hist_df = hist_df[hist_df["driverId"].isin(avg_score_df.loc[:2, "driverId"])]
order = avg_score_df.loc[:2, "driverName"].to_list()

scale = at.Scale(domain=order, range=["#FFD700", "#C0C0C0", "#CD7F32"])

chart = at.Chart(as_hist_df).encode(
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

avg_perf_df = goat_df.sort_values("meanOutperformance", ascending=False)
avg_perf_df = avg_perf_df[avg_perf_df["races"] >= 50].head(10).reset_index()
avg_perf_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_perf_df.shape[0] - 3)

st.markdown(f"# {avg_perf_df.loc[0, 'driverName']} is the outperformance GOAT")
st.markdown(f"For all races started, the driver's mean actual - expected performance (outperformance). Only drivers with >= 50 races considered.")

# create mean outperformance bar chart
chart = at.Chart(avg_perf_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("meanOutperformance", stack=None, title="Mean driver outperformance", scale=at.Scale(zero=False)),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("meanOutperformance:Q", format=".2f", title="Mean driver outperformance")
    ]
).properties(height=450)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color=theme["textColor"], align="left", dx=2).encode(
    text=at.Text("meanOutperformance:Q", format=".2f")
)

st.altair_chart(bars + text, use_container_width=True)

# create outperformance time series plot
ap_hist_df = hist_df[hist_df["driverId"].isin(avg_perf_df.loc[:2, "driverId"])]
order = avg_perf_df.loc[:2, "driverName"].to_list()

scale = at.Scale(domain=order, range=["#FFD700", "#C0C0C0", "#CD7F32"])

chart = at.Chart(ap_hist_df).encode(
    x=at.X("date", title="Date"),
    y=at.Y("outperformance", title="Driver outperformance", scale=at.Scale(zero=False)),
    color=at.Color("driverName", title="Driver name", sort=order, scale=scale),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("outperformance:Q", format=".2f", title="Driver outperformance")
    ]
)

lines = chart.mark_line()

st.altair_chart(lines, use_container_width=True)