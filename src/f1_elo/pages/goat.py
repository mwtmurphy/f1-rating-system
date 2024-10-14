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

    goat_df = pd.read_csv(CONFIG["data"]["goat_path"])
    hist_df = pd.read_csv(CONFIG["data"]["hist_path"])

    # create dataset for top 10 drivers
    avg_score_df = goat_df.sort_values("meanScore", ascending=False).head(10).reset_index(drop=True)
    avg_score_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_score_df.shape[0] - 3)

    # create dataset for top 3 drivers career plots
    as_hist_df = hist_df[hist_df["driverId"].isin(avg_score_df.loc[:2, "driverId"])]

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return avg_score_df, as_hist_df, last_race_dict


# streamlit page
avg_score_df, as_hist_df, last_race_dict = load_data()
st.info(f"Results as of: {last_race_dict['last_race']}")

# plot top 10 drivers based on mean career rating 
st.markdown(f"# {avg_score_df.loc[0, 'driverName']} is the rating GOAT")
st.markdown("Based on a driver's mean rating for all races started.")

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

# plot driver ratings for top 3 drivers over time
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
