import os

import dotenv
import pandas as pd

dotenv.load_dotenv()
ROOT_DIR = os.getenv("ROOT_DIR")
DATA_DIR = f"{ROOT_DIR}/data"

# CONSTRUCTOR_STATUSES = [
#     "engine", "transmission", "clutch", "electrical", "hydraulics", "gearbox", "radiator", 
#     "suspension", "brakes", "overheating", "mechanical", "tyre", "driver seat", "puncture", 
#     "driveshaft", "retired", "fuel pressure", "front wing", "water pressure", "refuelling", "wheel", 
#     "throttle", "steering", "technical", "electronics", "broken wing", "heat shield fire", "exhaust", 
#     "oil leak", "wheel rim", "water leak", "fuel pump", "track rod", "oil pressure", "pneumatics", 
#     "withdrew", "engine fire", "tyre puncture", "out of fuel", "wheel nut",
#     "handling", "rear wing", "fire", "fuel system", "oil line", "fuel rig", "launch control", 
#     "fuel", "power loss", "safety", "drivetrain", "ignition", "chassis", 
#     "battery", "halfshaft", "crankshaft", "safety concerns", "not restarted", "alternator", 
#     "differential", "wheel bearing", "physical", "vibrations", "underweight", "safety belt", 
#     "oil pump", "fuel leak", "excluded", "injection", "distributor", "turbo", 
#     "cv joint", "water pump", "spark plugs", "fuel pipe", "eye injury", "oil pipe", 
#     "axle", "water pipe", "magneto", "supercharger", "engine misfire", "ers", 
#     "power unit", "brake duct", "seat", "debris", "cooling system", "undertray"
# ]

# DRIVER_STATUSES = [
#     "collision", "collision damage", "accident", "disqualified", "spun off", "107% rule", 
#     "did not qualify", "stalled", "did not prequalify", "damage"
#     ]

# MISC_STATUSES = [
#     "driver unwell", "fatal accident", "illness", "injured", "injury", "not classified"
# ]

POINTS_MAP = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

def create_features():
    '''Exports features data to 'interim' data folder for creating
    model'''

    pre_df = pd.read_csv(f"{DATA_DIR}/interim/preprocessed_data.csv")

    # infer positions for non-finishers using qualifying position 
    car_df = pre_df[["year", "round", "grid"]].drop_duplicates()
    car_df["mapPosition"] = car_df.groupby(["year", "round"]).cumcount() + 1
    cle_df = pre_df.merge(car_df, on=["year", "round", "grid"], how="left")

    # create points scored with inferred positions
    cle_df["mapPoints"] = cle_df["mapPosition"].map(POINTS_MAP).fillna(0)

    # relabel race finish status
    #res_df["status"] = res_df["status"].apply(str.lower)
    #res_df["status"] = res_df["status"].apply(map_status)

    # remove columns no longer needed
    cle_df = cle_df.drop(columns=["grid", "position"])

    # export data
    cle_df.to_csv(f"{DATA_DIR}/interim/features.csv", index=False)

# def map_status(status: str) -> str:

#     if status == "finished" or "lap" in status:
#         return "finished"
#     elif status in DRIVER_STATUSES:
#         return "driver retirement"
#     elif status in CONSTRUCTOR_STATUSES:
#         return "constructor retirement"
#     elif status in MISC_STATUSES:
#         return "misc retirement"
#     else:
#         return status
    
if __name__=="__main__":
    create_features()



