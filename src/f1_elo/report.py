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

    # export data
    gott_df.to_csv(CONFIG["data"]["gott_path"], index=False)
    rank_df.to_csv(CONFIG["data"]["rank_path"], index=True)


if __name__=="__main__":
    make_report_data()
