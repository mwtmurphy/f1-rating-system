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

    # get drivers to be considered
    gott_df = vis_df.sort_values(["year", "round", "driverScore"], ascending=[True, True, False]).drop_duplicates(["year", "round"])
    gott_days = gott_df["driverId"].value_counts().iloc[:10]
    gott_drivers = set(gott_days.index)
    
    # create data to visualise greatest drivers over time
    gott_df = vis_df[vis_df["driverId"].isin(gott_drivers)].sort_values(["year", "round"])

    # create data for top ranked table
    rank_df = gott_days.reset_index()
    rank_df = rank_df.merge(drivers_df[["driverId", "driverName"]], on=["driverId"], how="left")
    rank_df = rank_df[["driverName", "count"]].rename(columns={
        "driverName": "Driver name",
        "count": "Races as top ranked"
    })
    rank_df.index += 1

    # get outcomes for 2024 
    df_24 = vis_df[vis_df["year"] == 2024]

    # create one-off data points
    
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
    gott_df.to_csv(CONFIG["data"]["gott_path"], index=False)
    rank_df.to_csv(CONFIG["data"]["rank_path"], index=True)
    df_24.to_csv(CONFIG["data"]["2024_path"], index=False)
    
    with open(CONFIG["data"]["one_off_path"], "w") as one_off_file:
        json.dump(one_off_dict, one_off_file)


if __name__=="__main__":
    make_report_data()
