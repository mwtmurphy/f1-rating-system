import json
import yaml

import pandas as pd
import plotly.express as px
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
    
    gott_df = pd.read_csv(CONFIG["data"]["gott_path"])
    rank_df = pd.read_csv(CONFIG["data"]["rank_path"], index_col=0)
    curr_df = pd.read_csv(CONFIG["data"]["2024_path"])

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return gott_df, rank_df, curr_df, one_off_dict

gott_df, rank_df, curr_df, one_off_dict = load_data()

# data visualisations
st.markdown("# How do the current drivers and teams rank?")
st.bar_chart

# st.markdown(
# f"""

# # Who is the F1 greatest of all time?

# A question that has ruined many a social event. There are many opinions but let's see what the data 
# has to say. From the first race in 1950 to the {one_off_dict['last_race']}, I've created a modified 
# version of the Elo rating system (used in chess) to score both drivers and constructors separately 
# to identify who is the F1 greatest of all time (GOAT).

# ## Method

# All drivers and constructors start with a score of 1500. Each win or loss vs a competitor increases 
# or decreases the scores of both the driver and constructor over time, the size of which is dependent 
# on the expected vs true outcome. I.e. a win over a higher-ranked driver-constructor pairing yields a 
# greater increase than a win over a lower-ranked driver-constructor paring.

# ## Results

# Taking the driver who ranks the higest per round, a count of races can be done as a basic estimate
# of the data GOAT... drumroll... who is... {rank_df["Driver name"].iloc[0]}! Cue disagreement.

# Here's how the top 10 performed over time:
# """
# )

# fig = px.line(gott_df, x="date", y="driverScore", color="driverName")
# st.plotly_chart(fig, use_container_width=True)

# st.markdown(
# f"""
# Here's a count of the races the top 10 ranked as highest rated driver:
# """
# )

# st.table(rank_df)

# st.markdown(
# f"""
# ## 2024 performance

# Explore the 2024 expected vs actual results so far. 

# Driver outperformance is calculated as the sum of the actual - expected scores for each driver. This
# allows us to see how they perform across rounds versus competitors.


# ### Driver performance
# """
# )

# dri_selected = st.selectbox("2024 driver", options=sorted(set(curr_df["driverName"])))
# dri_24_df = curr_df.loc[curr_df["driverName"] == dri_selected, ["round", "status", "expected", "actual"]]
# dri_24_df["outperformance"] = dri_24_df["actual"] - dri_24_df["expected"]
# dri_bar = st.bar_chart(dri_24_df, x="round", y="outperformance")
# dri_table = st.table(dri_24_df.set_index("round"))

# st.markdown(
# f"""
# ### Round performance
# """
# )

# round_selected = st.selectbox("2024 round", options=sorted(set(curr_df["round"])))
# sub_df = curr_df.loc[curr_df["round"] == round_selected, ["driverName", "status", "mapPosition", "expected", "actual"]]
# sub_df.columns = ["Driver name", "Race finish status", "Finishing position", "Expected score", "Actual score"]
# sub_df["Score outperformance"] = sub_df["Actual score"] - sub_df["Expected score"]
# sub_df = sub_df.set_index("Finishing position").sort_values("Score outperformance", ascending=False)
# round_table = st.table(sub_df)

# st.markdown(
# f"""
# ### Year performance
# """
# )

# avg_df = curr_df.groupby("driverName")[["expected", "actual"]].sum().reset_index()
# avg_df["Score outperformance"] = avg_df["actual"] - avg_df["expected"]
# avg_df = avg_df.sort_values("Score outperformance", ascending=False)
# avg_table = st.table(avg_df)


# st.markdown(
# f"""
# ## Limitations (non-exhaustive)

# 1. New drivers join the sport with different skill levels, so shouldn't all start at 1500.
# 2. New constructors can be rebranded or bought old constructors and should use their score vs starting
# again at 1500.
# """
# )