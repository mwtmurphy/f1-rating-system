import typing

import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def load_data(in_dir: str = "data/prod") -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
    '''Returns results and win loss dataframes for calculating ELO 
    scores'''

    res_df = pd.read_csv(f"{in_dir}/results.csv")
    wl_df = pd.read_csv(f"{in_dir}/win_loss.csv")

    return res_df, wl_df

load_state = st.text("Loading data...")
res_df, wl_df = load_data()
load_state.text(f"Data loaded!")

st.title("F1 Elo")

fig = px.line(res_df, x="date", y="score", color="driverId")
st.plotly_chart(fig)

