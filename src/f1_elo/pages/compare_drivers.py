import json
import yaml

import altair as at
import pandas as pd
import streamlit as st
import streamlit_theme

# set page config and theme
st.set_page_config(layout="wide")
theme = streamlit_theme.st_theme()

# load data config
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)

# load and cache data for visualisations
@st.cache_data
def load_data() -> tuple:
    '''Returns data for current driver plots'''

    # load data for comparing drivers
    hist_df = pd.read_csv(CONFIG["data"]["hist_path"])

    # load data recency json
    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return hist_df, last_race_dict

hist_df, last_race_dict = load_data()

# display data recency and sources
st.info(f"Results as of: {last_race_dict['last_race']}.")

# create dataframe for comparing drivers
selected_drivers = st.multiselect(label="Select drivers to compare.", options=sorted(list(set(hist_df["driverName"]))), default=["Max Verstappen", "Lando Norris"])
sd_sub_df = hist_df[hist_df["driverName"].isin(selected_drivers)]

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
