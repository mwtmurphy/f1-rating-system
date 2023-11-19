import pandas as pd
import plotly.express as px
import streamlit as st

# data import
@st.cache_data
def load_data(in_dir: str = "data/prod") -> tuple:
    '''Returns dataframe with ELO scores for drivers under GOAT 
    consideration and dataframe with days top ranked'''
    
    gott_df = pd.read_csv(f"{in_dir}/gott.csv")
    gott_days = pd.read_csv(f"{in_dir}/gott_days.csv")

    return gott_df, gott_days

gott_df, gott_days = load_data()

st.markdown(
"""
# F1 Elo

The question that has ruined many a social event: 

> Who is the F1 greatest of all time (GOAT)?  

There are many opinions. Is it Fangio, Senna, Michael Schumacher, Hamilton. Let's apply some data 
science to the problem to see if we can identify - at least - the data GOAT.

For races from 1986 Round 1 - 2023 Brazil, I've created Elo scores (used in chess) for all driver 
inter-team 1v1s due to identical vehicles. This allows to identify the greatest of their time drivers.

## Method

All drivers start with a score of 1500. With each win/loss this score increases/decreases over time. 
A win over a high-ranked teammate yields a greater increase than a win over a low-ranked teammate.

The degree of the win/loss also influences the score. If both drivers score points, their ranking will 
increase. If one driver scores 25 and the other 1 however, their increase is scaled respectively.

## Results

Taking drivers who were top ranked for at least 16 races (shortest season), this allows me to find
drivers to be considered the GOAT.
"""
)

fig = px.line(gott_df, x="date", y="score", color="driverId")
st.plotly_chart(fig)
st.table(gott_days)

st.markdown(
f"""
# The data GOAT = {gott_days['driverId'].iloc[0]}

## Limitations

This approach has clear limitations that are easy to spot:

1. Data begins at 1986, during some drivers careers.
2. Mechanical failures affect earlier seasons to a larger degree than
later seasons.
3. Drivers with longer careers have higher scores.
4. Seasons with more races give those drivers more chances to improve their scores.
5. Dominant cars give drivers an easier chance to score more points independent of skill.
6. Not all drivers join the sport with the same skill level, e.g. Hamilton was the F2 champion, Senna
was a 3x Formula Ford and F3 champion.

## Next steps

1. Add 1950 - 1985 data for teams with multiple drivers.
2. Add sprint races.
3. Add DNFs and type of DNFs (e.g. crashes = penalty, mechanical failures = no penalty).
4. Scale score change dependent on number of races in a season (less races = less chance to improve).
5. Add weighting dependent on constructors finishing position for year (e.g. expected points - realised points).
6. Add distance apart for finishers (points scored for 25s diff > points scored for 5s).
7. Scale initial Elo score dependent on racing history pre-F1.

"""
)