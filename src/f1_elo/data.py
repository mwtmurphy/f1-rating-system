import yaml

import pandas as pd

with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)

def preprocess_data():
    '''Exports preprocessed data to 'interim' data folder for creating
    features'''

    # merge raw data required for scoring
    results_df = pd.read_csv(CONFIG["data"]["results_csv"])
    races_df = pd.read_csv(CONFIG["data"]["races_csv"])
    con_yr_df = pd.read_csv(CONFIG["data"]["constructor_year_csv"])
    pre_df = races_df.merge(results_df, on="raceId", how="inner", validate="1:m").drop(columns=["raceId"])
    pre_df = pre_df.merge(con_yr_df[["constructorId", "year", "constructorYearId"]], on=["constructorId", "year"], how="left", validate="m:1")

    # preprocess data
    pre_df["position"] = pre_df["position"].replace("\\N", None).astype(float)

    col_order = ["year", "round", "date", "constructorId", "constructorYearId", "driverId", "grid", "position", "statusId"]
    sort_order = ["year", "round", "position", "grid"]
    pre_df = pre_df[col_order].sort_values(sort_order)

    pre_df.to_csv(CONFIG["data"]["preprocessed_path"], index=False)


if __name__=="__main__":
    preprocess_data()
