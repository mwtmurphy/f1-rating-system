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

    with open(CONFIG["data"]["one_off_path"], "r") as infile:
        one_off_dict = json.load(infile)

    return gott_df, rank_df, one_off_dict

gott_df, rank_df, one_off_dict = load_data()

# data vis
st.markdown(
f"""
*Last updated: {one_off_dict['last_race']}.*

# F1 Elo

The question that has ruined many a social event: 

> Who is the F1 greatest of all time (GOAT)?  

There are many opinions but let's apply some data science to the problem to see if we can identify 
the data GOAT.

From 1950 - 2024, I've created Elo scores for every constructor and driver for every race. This 
allows me to identify the drivers who were the greatest of their time.

## Method

All drivers and constructors start with a score of 1500. With each win/loss this increases/decreases 
the scores of both the constructor and driver over time, dependent on the expected vs realised outcome. 
E.g. a win over a high-ranked driver in a better car yields a greater increase than a win over a 
high-ranked driver in a worse car.

## Results

Taking drivers who were top ranked for 1 season, this allows me to find drivers to be considered.
"""
)

fig = px.line(gott_df, x="date", y="driverScore", color="driverName")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
"""
Counting the races these drivers ended up top ranked allows a simple guess at who is the data GOAT.
"""
)

st.table(rank_df)

st.markdown(
f"""
#### The data GOAT is {rank_df["Driver name"].iloc[0]}

## Limitations

1. New drivers do not join the sport with the same skill level, and shouldn't all start at 1500.
2. New constructors can be purchased old constructors and should use their score as their start score.
score.
3. Constructor scores do not account for major rule changes.

## Ideas to experiment with

1. Add sprint races to provide more ranking opportunities.
2. Add difference in points scored as Elo score influence.
3. Predictive model for expected outcome calculation.
"""
)