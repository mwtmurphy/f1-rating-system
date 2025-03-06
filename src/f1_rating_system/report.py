import json
import yaml

import pandas as pd


with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


def make_report_data() -> None:
    '''Creates and saves datasets to data/processed directory for use 
    in streamlit app'''

    mod_df = pd.read_csv(CONFIG["data"]["modelled_path"])
    col_df = pd.read_csv(CONFIG["data"]["colour_csv"])
    dri_df = pd.read_csv(CONFIG["data"]["drivers_csv"])
    con_df = pd.read_csv(CONFIG["data"]["constructors_csv"])
    raw_races_df = pd.read_csv(CONFIG["data"]["races_csv"])

    # map constructor and driver names to respective IDs
    dri_df["driverName"] = dri_df[["forename", "surname"]].apply(lambda row: " ".join(row), axis=1)
    res_df = mod_df.merge(dri_df[["driverId", "driverName"]], on=["driverId"], how="left")
    con_df = con_df.rename(columns={"name": "constructorName"})
    res_df = res_df.merge(con_df[["constructorId", "constructorName"]], on="constructorId", how="left")

    # create fields for analysis/reporting
    res_df["startDriScore"] = res_df.groupby("driverId")["driverScore"].shift().fillna(1500)
    res_df["driScoreChange"] = res_df["driverScore"] - res_df["startDriScore"]
    res_con_df = res_df[["year", "round", "constructorId", "constructorScore"]].drop_duplicates()
    res_con_df = res_con_df.sort_values(["year", "round"]).reset_index(drop=True)
    res_con_df["startConScore"] = res_con_df.groupby("constructorId")["constructorScore"].shift().fillna(1500)
    res_con_df = res_con_df.drop(columns=["constructorScore"])
    res_df = res_df.merge(res_con_df, on=["year", "round", "constructorId"], how="left")
    res_df["conScoreChange"] = res_df["constructorScore"] - res_df["startConScore"]
    res_df.to_csv(CONFIG["data"]["hist_path"])

    ## create dict for last race completed
    last_race_row = raw_races_df["date"] == mod_df["date"].max()
    last_race_ser = raw_races_df.loc[last_race_row, ["year", "name"]].iloc[0].tolist()
    last_race_dict = {"last_race": f"{last_race_ser[0]} {last_race_ser[1]}"}

    with open(CONFIG["data"]["last_race_path"], "w") as outfile:
        json.dump(last_race_dict, outfile)    
    
    # create dataset for top 10 drivers
    avg_goat_df = res_df.groupby(["driverId", "driverName"])["driverScore"].mean().reset_index()
    avg_goat_df = avg_goat_df.rename(columns={"driverScore": "meanScore"})
    avg_goat_df = avg_goat_df.sort_values("meanScore", ascending=False).head(10).reset_index(drop=True)
    avg_goat_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_goat_df.shape[0] - 3)
    avg_goat_df.to_csv(CONFIG["data"]["avg_goat_path"], index=False)

    # create dataset for top 3 drivers career plots
    avg_hist_df = res_df[res_df["driverId"].isin(avg_goat_df.loc[:2, "driverId"])]
    avg_hist_df.to_csv(CONFIG["data"]["avg_hist_path"], index=False)

    # create current driver rating data
    cur_yr_df = res_df[res_df["year"] == res_df["year"].max()]
    cur_yr_df = cur_yr_df.merge(col_df, how="left", on="constructorId")

    cur_round_row = cur_yr_df["round"] == cur_yr_df["round"].max()
    cur_dri_df = cur_yr_df.loc[cur_round_row, ["constructorId", "driverName", "driverScore", "hex_code"]]
    cur_dri_df = cur_dri_df.sort_values("driverScore", ascending=False).reset_index(drop=True)
    cur_dri_df.to_csv(CONFIG["data"]["cur_dri_path"], index=False)

    # create driver rating improvement data
    dri_imp_df = cur_yr_df.copy()
    dri_imp_df["cumDriScoreChange"] = dri_imp_df.groupby("driverId")["driScoreChange"].cumsum()
    dri_imp_df = dri_imp_df.sort_values("round").drop_duplicates("driverId", keep="last")
    dri_imp_df = dri_imp_df.sort_values("cumDriScoreChange", ascending=False)
    dri_imp_df = dri_imp_df[["driverName", "cumDriScoreChange", "hex_code"]].reset_index(drop=True)
    dri_imp_df["baseline"] = 0
    dri_imp_df.to_csv(CONFIG["data"]["dri_imp_path"], index=False)

    # create current constructor rating data
    cur_con_df = cur_yr_df.loc[cur_round_row, ["constructorId", "constructorName", "constructorScore", "hex_code"]]
    cur_con_df = cur_con_df.drop_duplicates().sort_values("constructorScore", ascending=False).reset_index(drop=True)
    cur_con_df.to_csv(CONFIG["data"]["cur_con_path"], index=False)

    # create constructor rating improvement data
    con_imp_df = cur_yr_df[["constructorId", "constructorName", "conScoreChange", "hex_code"]].drop_duplicates()
    con_imp_df = con_imp_df.groupby(["constructorId", "constructorName", "hex_code"])["conScoreChange"].sum().reset_index()
    con_imp_df = con_imp_df.sort_values("conScoreChange", ascending=False).reset_index(drop=True)
    con_imp_df["baseline"] = 0
    con_imp_df.to_csv(CONFIG["data"]["con_imp_path"], index=False)


if __name__=="__main__":
    make_report_data()
