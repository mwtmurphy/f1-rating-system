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

    dri_hist_df = pd.read_csv(CONFIG["data"]["hist_path"])

    with open(CONFIG["data"]["last_race_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return dri_hist_df, last_race_dict


# streamlit app
dri_hist_df, last_race_dict = load_data()
st.info(f"Results as of: {last_race_dict['last_race']}.")

# create dataframe for comparing drivers based on user selection
selected_drivers = st.multiselect(label="Select drivers to compare.", options=sorted(list(set(dri_hist_df["driverName"]))), default=["Max Verstappen", "Lando Norris"])
sd_sub_df = dri_hist_df[dri_hist_df["driverName"].isin(selected_drivers)]

# plot comparison over career timeline
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
