import os

import dotenv
import pandas as pd

dotenv.load_dotenv()
ROOT_DIR = os.getenv("ROOT_DIR")
DATA_DIR = f"{ROOT_DIR}/data"

def preprocess_data():
    '''Exports preprocessed data to 'interim' data folder for creating
    features'''

    # merge raw data required for scoring
    results_df = pd.read_csv(f"{DATA_DIR}/raw/results.csv")
    races_df = pd.read_csv(f"{DATA_DIR}/raw/races.csv")
    pre_df = races_df.merge(results_df, on="raceId", how="inner", validate="1:m").drop(columns=["raceId"])

    # preprocess data
    pre_df["position"] = pre_df["position"].replace("\\N", None).astype(float)

    col_order = ["year", "round", "date", "constructorId", "driverId", "grid", "position"]#, "statusId"]
    sort_order = ["year", "round", "position", "grid"]
    pre_df = pre_df[col_order].sort_values(sort_order)

    pre_df.to_csv(f"{DATA_DIR}/interim/preprocessed_data.csv", index=False)

if __name__=="__main__":
    preprocess_data()

# CODE TO BE USED AT A LATER DATE

#drivers_df = pd.read_csv(f"{DATA_DIR}/drivers.csv")[["driverId", "driverRef"]]
#constructors_df = pd.read_csv(f"{DATA_DIR}/constructors.csv")[["constructorId", "constructorRef"]]
#status_df = pd.read_csv(f"{DATA_DIR}/status.csv")

#raw_df = raw_df.merge(drivers_df, on="driverId", how="left")
#raw_df = raw_df.merge(constructors_df, on="constructorId", how="left")
#raw_df = raw_df.merge(status_df, on="statusId", how="left")

#raw_df = raw_df[["year", "round", "date", "constructorRef", "driverRef", "grid", "position", "status"]]