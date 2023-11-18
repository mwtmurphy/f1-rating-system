import pandas as pd
import plotly.express as px
import streamlit as st

# data import
@st.cache_data
def load_data(in_dir: str = "data/prod") -> pd.DataFrame:
    '''Returns results dataframe with ELO scores'''
    return pd.read_csv(f"{in_dir}/results.csv")

res_df = load_data()

st.title("F1 Elo")

# user input
years = st.multiselect("Race years to display", list(set(res_df["year"])), default=[2023])

# data cleaning
sub_df = res_df.copy()
if years:
    drivers = list(set(sub_df.loc[sub_df["year"].isin(years), "driverId"]))
    sub_df = sub_df[sub_df["driverId"].isin(drivers)]
sub_df = sub_df.sort_values(["year", "round"])

# data cleaning - 2023 analysis
drivers = set(res_df.loc[res_df["year"] == 2023, "driverId"])
cur_df = res_df[(res_df["year"] == 2023) & res_df["driverId"].isin(drivers)]
round_df = cur_df.groupby("driverId")["round"].describe()[["min", "max"]].reset_index()

for ix, row in round_df.iterrows():
    score_1 = cur_df.loc[(cur_df["driverId"] == row["driverId"]) & (cur_df["round"] == row["min"]), "score"].iloc[0]
    score_2 = cur_df.loc[(cur_df["driverId"] == row["driverId"]) & (cur_df["round"] == row["max"]), "score"].iloc[0]

    round_df.loc[round_df["driverId"] == row["driverId"], "min"] = score_1
    round_df.loc[round_df["driverId"] == row["driverId"], "max"] = score_2

round_df["change"] = round_df["max"] - round_df["min"]
round_df.columns = ["Driver ID", "First round ELO", "Last round ELO", "Change"]
round_df = round_df.set_index("Driver ID").sort_values("Change", ascending=False)

# data cleaning - GOATs
goat_df = res_df.sort_values(["year", "round", "score"], ascending=[True, True, False]).drop_duplicates(['year','round'])
goat_df = goat_df["driverId"].value_counts().reset_index().head(10)
goat_df.columns = ["Driver ID", "Number of races"]

# data vis
fig = px.line(sub_df, x="date", y="score", color="driverId")
st.plotly_chart(fig)

st.title("Best perfomers in 2023")
st.table(round_df)

st.title("Races as greatest driver active")
st.table(goat_df)