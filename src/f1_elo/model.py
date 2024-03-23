import itertools
import json
import typing
import yaml

import bayes_opt
import pandas as pd


with open("params.yaml") as conf_file:
    CONFIG = yaml.safe_load(conf_file)


def model_data(k: float, c: float, w: float, export: bool = False) -> typing.Union[float, None]:
    '''If export == False, returns negative RMSEE based on params. 
    If export == True, exports modelled data to 'interim' data folder 
    for data reporting.'''

    cle_df = pd.read_csv(CONFIG["data"]["features_path"])
    dri_scores = {id: CONFIG["model"]["start_score"] for id in set(cle_df["driverId"])}
    con_scores = {id: CONFIG["model"]["start_score"] for id in set(cle_df["constructorId"])}
    cle_df[["constructorScore", "driverScore"]] = None
    exp, out = [], []

    yr_df = cle_df[["year", "round"]].drop_duplicates()
    for _, (yr, rnd) in yr_df.iterrows():
        valid_ix = (cle_df["year"] == yr) & (cle_df["round"] == rnd)
        sub_ix = valid_ix & (cle_df["status"].isin(["finished", "driver retirement"]))
        
        rnd_dri_scores = {dri: {"diff": 0, "n": 0} for dri in cle_df.loc[sub_ix, "driverId"]}
        rnd_con_scores = {dri: {"diff": 0, "n": 0} for dri in cle_df.loc[sub_ix, "constructorId"]}

        for ix_1, ix_2 in itertools.combinations(cle_df[sub_ix].index, 2):
            dri_a = cle_df.loc[ix_1, "driverId"]
            con_a = cle_df.loc[ix_1, "constructorId"]
            elo_a = dri_scores[dri_a] + (w * con_scores[con_a])
            pos_a = cle_df.loc[ix_1, "mapPosition"]

            dri_b = cle_df.loc[ix_2, "driverId"]
            con_b = cle_df.loc[ix_2, "constructorId"]
            elo_b = dri_scores[dri_b] + (w * con_scores[con_b])
            pos_b = cle_df.loc[ix_2, "mapPosition"]

            # continue if drivers in same car
            if pos_a == pos_b:
                continue

            # calculate position influence
            q_a = 10 ** (elo_a / c)
            q_b = 10 ** (elo_b / c)
    
            e_a = q_a / (q_a + q_b)        
            e_b = q_b / (q_a + q_b)

            # score outcome
            if pos_a < pos_b:
                o_a = 1
                o_b = 0
            else:
                o_a = 0
                o_b = 1
                
            # calculate score change and update round scores
            diff_a = k * (o_a - e_a)
            diff_b = k * (o_b - e_b)

            rnd_con_scores[con_a]["diff"] += diff_a
            rnd_con_scores[con_a]["n"] += 1
            rnd_dri_scores[dri_a]["diff"] += diff_a
            rnd_dri_scores[dri_a]["n"] += 1

            rnd_con_scores[con_b]["diff"] += diff_b
            rnd_con_scores[con_b]["n"] += 1
            rnd_dri_scores[dri_b]["diff"] += diff_b
            rnd_dri_scores[dri_b]["n"] += 1

            # store expected and final values
            exp += [e_a, e_b]
            out += [o_a, o_b]
        
        # update driver elo scores for finishing drivers and driver-caused retirements
        for dri in rnd_dri_scores.keys():
            if rnd_dri_scores[dri]["n"] != 0: # more than 1 car on grid
                dri_scores[dri] += (rnd_dri_scores[dri]["diff"] / rnd_dri_scores[dri]["n"])
                
        cle_df.loc[valid_ix, "driverScore"] = cle_df.loc[valid_ix, "driverId"].map(dri_scores)

        # update constructor elo scores for finishing drivers
        for con in rnd_con_scores.keys():
            if rnd_con_scores[con]["n"] != 0: # more than 1 car on grid
                con_scores[con] += (rnd_con_scores[con]["diff"] / rnd_con_scores[con]["n"])
        
        cle_df.loc[valid_ix, "constructorScore"] = cle_df.loc[valid_ix, "constructorId"].map(con_scores)
    
    if export == False:
        err_df = pd.DataFrame({"pred": exp, "true": out})
        err_df["squared_error"] = (err_df["true"] - err_df["pred"]) ** 2
        neg_rmse = -(pow(err_df["squared_error"].sum() / err_df.shape[0], 0.5))
        return neg_rmse
    
    else:    
        cle_df.to_csv(CONFIG["data"]["modelled_path"], index=False)


if __name__=="__main__":

    # find optimal parameters
    opt_params = CONFIG["model"]["opt_params"]
    optimiser = bayes_opt.BayesianOptimization(
        f=model_data,
        pbounds=opt_params["pbounds"],
        random_state=opt_params["random_state"],
        allow_duplicate_points=True
    )

    optimiser.maximize(
        init_points=opt_params["init_points"], 
        n_iter=opt_params["n_iter"]
    )
    results = optimiser.max
    params_log = {
        "k": float(results["params"]["k"]),
        "c": float(results["params"]["c"]),
        "w": float(results["params"]["w"])
    }
    metrics_log = {
        "RMSE": float(-results["target"])
    }

    #log metrics and params locally
    with open(CONFIG["data"]["metrics_path"], "w") as out:
        json.dump(metrics_log, out)

    with open(CONFIG["data"]["params_path"], "w") as out:
        yaml.dump(params_log, out)

    # create final model data
    model_data(k=params_log["k"], c=params_log["c"], w=params_log["w"], export=True)
