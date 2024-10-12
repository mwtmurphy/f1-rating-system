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

    # load data for comparing constructors
    hist_df = pd.read_csv(CONFIG["data"]["hist_path"])
    con_df = hist_df[["date", "constructorId", "constructorName", "constructorScore"]].drop_duplicates()

    # load data recency json
    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        last_race_dict = json.load(infile)

    return con_df, last_race_dict

con_df, last_race_dict = load_data()

# display data recency and sources
st.info(f"Results as of: {last_race_dict['last_race']}.")

# create dataframe for comparing constructors
selected_constructors = st.multiselect(label="Select constructors to compare.", options=sorted(list(set(con_df["constructorName"]))), default=["Red Bull", "McLaren"])
sd_sub_df = con_df[con_df["constructorName"].isin(selected_constructors)]

# plot comparison over career timeline
line_chart = at.Chart(sd_sub_df).mark_line().encode(
    x=at.X("date", stack=None, title="Date"),
    y=at.Y("constructorScore", sort=None, title="Constructor rating", scale=at.Scale(zero=False)),
    color=at.Text("constructorName", title="Constructor"),
    tooltip=[
        at.Tooltip("constructorName", title="Constructor"),
        at.Tooltip("constructorScore:Q", format=".0f", title="Rating"),
        at.Tooltip("date", title="Date")
    ]
)

st.altair_chart(line_chart, use_container_width=True)
