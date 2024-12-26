import itertools
import json
import typing
import yaml

import bayes_opt
import numpy as np
import pandas as pd
from scipy import optimize


# global variables
with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)

# column indexes
CON_IX = 4 # constructor id
DRI_IX = 5 # driver id
POS_IX = 6 # driver position
STA_IX = 8 # race status
CSC_IX = 9 # new constructor score
DSC_IX = 10 # new driver score
EXP_IX = 11 # expected outcome
TRU_IX = 12 # true outcome

MOD_DF = pd.read_csv(CONFIG["data"]["features_path"])
MOD_DF[["constructorScore", "driverScore", "expected", "actual"]] = None
IX_CHUNKS = MOD_DF.reset_index().groupby(["year", "round"])["index"].agg(["min", "max"]).values
MOD_MAT = MOD_DF.values

DRI_RTG = {dri: CONFIG["model"]["start_score"] for dri in set(MOD_DF["driverId"])}
CON_RTG = {con: CONFIG["model"]["start_score"] for con in set(MOD_DF["constructorYearId"])}

def model_data(params: dict, export: bool = False) -> float:
    '''Returns mean negative log likelihood of the rating system. If
    export = True, also exports results for data reporting.'''

    dri_scores = DRI_RTG.copy()
    con_scores = CON_RTG.copy()
    exp, out = [], []
    log_likelihood = 0
    n_pred = 0

    for start_ix, end_ix in IX_CHUNKS:
        yr_mat = MOD_MAT[start_ix:end_ix+1]

        rnd_dri_scores = {dri: {"diff": 0, "n": 0, "exp": 0, "act": 0} for dri in yr_mat[:, DRI_IX]}
        rnd_con_scores = {con: {"diff": 0, "n": 0, "exp": 0, "act": 0} for con in yr_mat[:, CON_IX]}

        for ix_1, ix_2 in itertools.combinations(range(yr_mat.shape[0]), 2):
            con_a, dri_a, pos_a, st_a = yr_mat[ix_1, [CON_IX, DRI_IX, POS_IX, STA_IX]]
            con_b, dri_b, pos_b, st_b = yr_mat[ix_2, [CON_IX, DRI_IX, POS_IX, STA_IX]]
    
            # continue if drivers in same car or a driver does not finish for misc reason
            if pos_a == pos_b or "misc retirement" in [st_a, st_b]:
                continue

            # get current rating
            elo_a = dri_scores[dri_a] + (params[2] * con_scores[con_a])
            elo_b = dri_scores[dri_b] + (params[2] * con_scores[con_b])
            
            # create expected scores
            e_a = 1 / (1 + np.exp(-(elo_a - elo_b) / params[1]))
            e_b = 1 - e_a

            # create true scores and track log likelihood 
            if pos_a < pos_b:
                o_a = 1
                o_b = 0
                log_likelihood += np.log(max(e_a, 1E-10))

            else:
                o_a = 0
                o_b = 1
                log_likelihood += np.log(max(e_b, 1E-10))

            n_pred += 1
                
            # calculate score change and update round scores
            diff_a = params[0] * (o_a - e_a)
            diff_b = params[0] * (o_b - e_b)

            # log driver results and changes if neither retire due to car failure (not attributable to drivers)
            if "constructor retirement" not in [st_a, st_b]:
                rnd_dri_scores[dri_a]["exp"] += e_a
                rnd_dri_scores[dri_a]["act"] += o_a
                rnd_dri_scores[dri_a]["diff"] += diff_a
                rnd_dri_scores[dri_a]["n"] += 1

                rnd_dri_scores[dri_b]["exp"] += e_b
                rnd_dri_scores[dri_b]["act"] += o_b
                rnd_dri_scores[dri_b]["diff"] += diff_b
                rnd_dri_scores[dri_b]["n"] += 1
            
            # log constructor changes if diff constructors and neither driver retires due to driver error (not attributable to constructors)
            if con_a != con_b and "driver retirement" not in [st_a, st_b]:
                rnd_con_scores[con_a]["diff"] += diff_a
                rnd_con_scores[con_a]["n"] += 1
    
                rnd_con_scores[con_b]["diff"] += diff_b
                rnd_con_scores[con_b]["n"] += 1
                
            # store expected and final values for error analysis
            exp += [e_a, e_b]
            out += [o_a, o_b]
        
        # update driver values for finishing drivers and driver-caused retirements
        for dri in rnd_dri_scores.keys():
            if rnd_dri_scores[dri]["n"] != 0: # more than 1 car on grid
                dri_scores[dri] += ((1 / (1 + params[2])) * rnd_dri_scores[dri]["diff"] / rnd_dri_scores[dri]["n"])

        yr_mat[:, DSC_IX] = list(map(lambda el: dri_scores[el], yr_mat[:, DRI_IX])) # driver score
        yr_mat[:, EXP_IX] = list(map(lambda el: rnd_dri_scores[el]["exp"], yr_mat[:, DRI_IX])) # expected outcome
        yr_mat[:, TRU_IX] = list(map(lambda el: rnd_dri_scores[el]["act"], yr_mat[:, DRI_IX])) # actual outcome

        # update constructor values for finishing drivers
        for con in rnd_con_scores.keys():
            if rnd_con_scores[con]["n"] != 0: # more than 1 car on grid
                con_scores[con] += ((params[2] / (1 + params[2])) * rnd_con_scores[con]["diff"] / rnd_con_scores[con]["n"])
        
        yr_mat[:, CSC_IX] = list(map(lambda el: con_scores[el], yr_mat[:, CON_IX]))

    if export:
        RES_DF = pd.DataFrame(MOD_MAT, columns=MOD_DF.columns)
        RES_DF.to_csv(CONFIG["data"]["modelled_path"], index=False)
        return - log_likelihood / n_pred

    else:   
        return - log_likelihood / n_pred        

if __name__=="__main__":

    params = [
        0.5, # K-factor - sensitivity of score change
        400, # C-factor - sensitivity of expected outcome
        0.5  # Driver-constructor weighting
    ] 

    result = optimize.minimize(model_data, params, method="L-BFGS-B", options={"disp": True})

    params_log = {
        "k": result.x[0],
        "c": result.x[1],
        "w": result.x[2]
    }

    metrics_log = {
        "log_likelihood": model_data(result.x, export=True) # exports results for data reporting also
    }

    #log metrics and params
    with open(CONFIG["data"]["metrics_path"], "w") as out:
        json.dump(metrics_log, out)

    with open(CONFIG["data"]["params_path"], "w") as out:
        yaml.dump(params_log, out)
