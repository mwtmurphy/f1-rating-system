import json
import yaml

import altair as at
import pandas as pd
import streamlit as st

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

goat_df, hist_df, one_off_dict = load_data()

avg_score_df = goat_df.sort_values("meanScore", ascending=False).head(10).reset_index(drop=True)
avg_score_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_score_df.shape[0] - 3)

st.info(f"Results as of: {one_off_dict['last_race']}")

st.markdown(f"# {avg_score_df.loc[0, 'driverName']} is the rating GOAT")
st.markdown("For all races started, the driver's mean rating.")

chart = at.Chart(avg_score_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("meanScore", title="Mean driver rating"),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("meanScore:Q", format=".0f", title="Mean driver score")
    ]
).properties(height=450)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color="black", align="left", dx=2).encode(
    text=at.Text("meanScore:Q", format=".0f")
)



st.altair_chart(bars + text, use_container_width=True)

avg_perf_df = goat_df.sort_values("meanOutperformance", ascending=False)
avg_perf_df = avg_perf_df[avg_perf_df["races"] >= 50].head(10).reset_index()
avg_perf_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_perf_df.shape[0] - 3)

st.markdown(f"# {avg_perf_df.loc[0, 'driverName']} is the outperformance GOAT")
st.markdown(f"For all races started, the driver's mean actual - expected performance (outperformance). Only drivers with >= 50 races considered.")


chart = at.Chart(avg_perf_df).encode(
    y=at.Y("driverName", sort=None, title="Driver name"),
    x=at.X("meanOutperformance", title="Mean driver outperformance"),
    tooltip=[
        at.Tooltip("driverName", title="Driver name"),
        at.Tooltip("meanOutperformance:Q", format=".2f", title="Mean driver outperformance")
    ]
).properties(height=450)

bars = chart.mark_bar(size=30).encode(
    color=at.Color("hex_code:N", scale=None)
)

text = chart.mark_text(color="black", align="left", dx=2).encode(
    text=at.Text("meanOutperformance:Q", format=".2f")
)

st.altair_chart(bars + text, use_container_width=True)