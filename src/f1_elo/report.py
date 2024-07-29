import json
import yaml

import pandas as pd


with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


def make_report_data():

    mod_df = pd.read_csv(CONFIG["data"]["modelled_path"])

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
    
    ## get last race completed
    completed_race_ids = set(pd.read_csv(CONFIG["data"]["results_csv"])["raceId"])
    races_df = pd.read_csv(CONFIG["data"]["races_csv"])
    races_df = races_df[races_df["raceId"].isin(completed_race_ids)]
    latest_race_ser = races_df.loc[races_df["date"] == races_df["date"].max(), ["year", "name"]].iloc[0].tolist()
    latest_race = f"{latest_race_ser[0]} {latest_race_ser[1]}"

    one_off_dict = {
        "last_race": latest_race
    }

    # export data
    goat_df.to_csv(CONFIG["data"]["goat_path"], index=False)
    hist_df.to_csv(CONFIG["data"]["hist_path"], index=True)
    df_24.to_csv(CONFIG["data"]["2024_path"], index=False)
    
    with open(CONFIG["data"]["one_off_path"], "w") as one_off_file:
        json.dump(one_off_dict, one_off_file)


if __name__=="__main__":
    make_report_data()
