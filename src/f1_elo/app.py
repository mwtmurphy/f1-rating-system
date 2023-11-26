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

    return gott_df, rank_df

gott_df, rank_df = load_data()

# data vis
st.markdown(
"""
# F1 Elo

The question that has ruined many a social event: 

> Who is the F1 greatest of all time (GOAT)?  

There are many opinions. Is it Fangio, Senna, Michael Schumacher, Hamilton. Let's apply some data 
science to the problem to see if we can identify - at least - the data GOAT.

For races from 1950 - 2023 Brazil, I've created Elo scores (used in chess) for all driver 
inter-team 1v1s due to identical vehicles. This allows to identify the greatest of their time drivers.

## Method

All drivers start with a score of 1500. With each win/loss this score increases/decreases over time. 
A win over a high-ranked teammate yields a greater increase than a win over a low-ranked teammate.

The degree of the win/loss also influences the score. If both drivers score points, their ranking will 
increase. If one driver scores 25 and the other 1 however, their increase is scaled respectively.

## Results

Taking drivers who were top ranked for 1 season, this allows me to find
drivers to be considered the GOAT.
"""
)

fig = px.line(gott_df, x="date", y="elo_score", color="driverName")
st.plotly_chart(fig, use_container_width=True)
st.table(rank_df.iloc[:10])

st.markdown(
f"""
# The data GOAT = {rank_df["Driver name"].iloc[0]}

## Limitations

1. Driver and non-driver retirements aren't accounted for.
2. Drivers with longer careers have higher scores.
3. Dominant cars give drivers an easier chance to score more points independent of skill.
4. Not all drivers join the sport with the same skill level, e.g. Hamilton was an F2 and F3 champion, Senna
was a 3x Formula Ford and F3 champion.

## Next steps

1. Add sprint races.
2. Add DNFs and type of DNFs (e.g. crashes = penalty, mechanical failures = no penalty).
3. Add weighting dependent on constructors finishing position for year (e.g. expected points - realised points).
4. Add distance apart for finishers (points scored for 25s diff > points scored for 5s).
5. Scale initial Elo score dependent on racing history pre-F1.
"""
)