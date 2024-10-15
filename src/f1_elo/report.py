import json
import yaml

import pandas as pd


with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


def make_report_data():

    mod_df = pd.read_csv(CONFIG["data"]["modelled_path"])
    col_df = pd.read_csv(CONFIG["data"]["colour_csv"])

    # replace driver ID with driver name for visualisation
    drivers_df = pd.read_csv(CONFIG["data"]["drivers_csv"])[["driverId", "forename", "surname"]]
    drivers_df["driverName"] = drivers_df[["forename", "surname"]].apply(lambda row: " ".join(row), axis=1)
    vis_df = mod_df.merge(drivers_df[["driverId", "driverName"]], on=["driverId"], how="left")

    con_df = pd.read_csv(CONFIG["data"]["constructors_csv"])[["constructorId", "name"]]
    con_df = con_df.rename(columns={"name": "constructorName"})
    vis_df = vis_df.merge(con_df, on="constructorId", how="left")

    # create data for vis'
    vis_df["startDriScore"] = vis_df.groupby("driverId")["driverScore"].shift().fillna(1500)
    vis_con_df = vis_df[["year", "round", "constructorId", "constructorScore"]].drop_duplicates().sort_values(["year", "round"]).reset_index(drop=True)
    vis_con_df["startConScore"] = vis_con_df.groupby("constructorId")["constructorScore"].shift().fillna(1500)
    vis_con_df = vis_con_df.drop(columns=["constructorScore"])
    vis_df = vis_df.merge(vis_con_df, on=["year", "round", "constructorId"], how="left")
    vis_df["driScoreChange"] = vis_df["driverScore"] - vis_df["startDriScore"]
    vis_df["conScoreChange"] = vis_df["constructorScore"] - vis_df["startConScore"]

    # get drivers to be considered
    vis_df["outperformance"] = vis_df["actual"] - vis_df["expected"]
    out_df = vis_df.groupby("driverId")["outperformance"].mean().reset_index().rename(columns={"outperformance": "meanOutperformance"})
    count_df = vis_df.groupby("driverId").size().reset_index().rename(columns={0: "races"})
    max_df = vis_df.groupby("driverId")["driverScore"].max().reset_index().rename(columns={"driverScore": "maxScore"})

    agg_df = vis_df.groupby(["driverId", "driverName"])["driverScore"].mean().reset_index().rename(columns={"driverScore": "meanScore"})
    agg_df = agg_df.merge(out_df, on="driverId", how="left").merge(count_df, on="driverId", how="left").merge(max_df, on="driverId", how="left")
    agg_df = agg_df[["driverId", "driverName", "races", "meanScore", "meanOutperformance", "maxScore"]]

    goat_df = agg_df
    hist_df = vis_df

    # get outcomes for 2024 
    df_24 = vis_df[vis_df["year"] == 2024]

    hist_df.to_csv(CONFIG["data"]["hist_path"])
    
    ## get last race completed
    completed_race_ids = set(pd.read_csv(CONFIG["data"]["results_csv"])["raceId"])
    races_df = pd.read_csv(CONFIG["data"]["races_csv"])
    races_df = races_df[races_df["raceId"].isin(completed_race_ids)]
    latest_race_ser = races_df.loc[races_df["date"] == races_df["date"].max(), ["year", "name"]].iloc[0].tolist()
    last_race_dict = {"last_race": f"{latest_race_ser[0]} {latest_race_ser[1]}"}

    with open(CONFIG["data"]["last_race_path"], "w") as outfile:
        json.dump(last_race_dict, outfile)    
    
    # create dataset for top 10 drivers
    avg_goat_df = goat_df.sort_values("meanScore", ascending=False).head(10).reset_index(drop=True)
    avg_goat_df["hex_code"] = ["#FFD700", "#C0C0C0", "#CD7F32"] + ["#F7EAB4"] * (avg_goat_df.shape[0] - 3)
    avg_goat_df.to_csv(CONFIG["data"]["avg_goat_path"], index=False)

    # create dataset for top 3 drivers career plots
    avg_hist_df = hist_df[hist_df["driverId"].isin(avg_goat_df.loc[:2, "driverId"])]
    avg_hist_df.to_csv(CONFIG["data"]["avg_hist_path"], index=False)

    # create current driver rating data
    cur_dri_df = df_24.loc[df_24["round"] == df_24["round"].max(), ["constructorId", "driverName", "driverScore"]].sort_values("driverScore", ascending=False).reset_index(drop=True)
    cur_dri_df = cur_dri_df.merge(col_df, how="left", on="constructorId")
    cur_dri_df.to_csv(CONFIG["data"]["cur_dri_path"], index=False)

    # create driver rating improvement data
    dri_imp_df = df_24.copy()
    dri_imp_df["cumDriScoreChange"] = dri_imp_df.groupby("driverId")["driScoreChange"].cumsum()
    dri_imp_df = dri_imp_df.sort_values("round").drop_duplicates("driverId", keep="last")[["constructorId", "driverName", "cumDriScoreChange"]]
    dri_imp_df = dri_imp_df.merge(col_df, how="left", on="constructorId").sort_values("cumDriScoreChange", ascending=False)
    dri_imp_df = dri_imp_df.reset_index(drop=True).drop(columns="constructorId")
    dri_imp_df["baseline"] = 0
    dri_imp_df.to_csv(CONFIG["data"]["dri_imp_path"], index=False)

    # create current constructor rating data
    cur_con_df = df_24.loc[df_24["round"] == df_24["round"].max(), ["constructorId", "constructorName", "constructorScore"]].drop_duplicates().sort_values("constructorScore", ascending=False).reset_index(drop=True)
    cur_con_df = cur_con_df.merge(col_df, how="left", on="constructorId")
    cur_con_df.to_csv(CONFIG["data"]["cur_con_path"], index=False)

    # create constructor rating improvement data
    con_imp_df = df_24[["constructorId", "constructorName", "conScoreChange"]].drop_duplicates().groupby(["constructorId", "constructorName"])["conScoreChange"].sum().reset_index()
    con_imp_df = con_imp_df.merge(col_df, how="left", on="constructorId").sort_values("conScoreChange", ascending=False).reset_index(drop=True)
    con_imp_df["baseline"] = 0
    con_imp_df.to_csv(CONFIG["data"]["con_imp_path"], index=False)


if __name__=="__main__":
    make_report_data()
