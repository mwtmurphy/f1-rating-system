import itertools
import os

import bayes_opt
import dotenv
import dvclive
import pandas as pd


dotenv.load_dotenv()
ROOT_DIR = os.getenv("ROOT_DIR")
DATA_DIR = f"{ROOT_DIR}/data"


def model_data(k: float, c: float, export: bool = False) -> float:
    '''If export == False, returns negative SSE based on k and c. If
    export == True, exports modelled data to 'interim' data folder for 
    data reporting.'''

    cle_df = pd.read_csv(f"{DATA_DIR}/interim/features.csv")
    elo_scores = {id: 1500 for id in set(cle_df["driverId"])}
    yr_rounds = cle_df.groupby("year")["round"].nunique()
    cle_df["elo_score"] = None
    exp, out = [], []
    #l = 40

    yrc_df = cle_df[["year", "round", "constructorId"]].drop_duplicates()
    for _, (yr, rnd, ctr) in yrc_df.iterrows():
        valid_ix = (cle_df["year"] == yr) & (cle_df["round"] == rnd) & (cle_df["constructorId"] == ctr)
        sub_df = cle_df[valid_ix]

        round_scores = {dvr: {"diff": 0, "n": 0} for dvr in sub_df["driverId"]}
        for ix_1, ix_2 in itertools.combinations(sub_df.index, 2):
            dvr_a = cle_df.loc[ix_1, "driverId"]
            elo_a = elo_scores[dvr_a]
            pos_a = cle_df.loc[ix_1, "mapPosition"]
            #poi_a = cle_df.loc[ix_1, "mapPoints"]

            dvr_b = cle_df.loc[ix_2, "driverId"]
            elo_b = elo_scores[dvr_b]
            pos_b = cle_df.loc[ix_2, "mapPosition"]
            #poi_b = cle_df.loc[ix_2, "mapPoints"]

            # continue if drivers in same car
            if pos_a == pos_b:
                continue

            # calculate points influence
            # if poi_a + poi_b == 0:
            #     s_a = 0.5
            #     s_b = 0.5
            # else:
            #     s_a = poi_a / (poi_a + poi_b)
            #     s_b = poi_b / (poi_a + poi_b)

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
                
            # calculate score change and update round_scores
            diff_a = ((k ) * (o_a - e_a)) #+ ((l / yr_rounds[yr]) * s_a)
            diff_b = ((k ) * (o_b - e_b)) #+ ((l / yr_rounds[yr]) * s_b)

            round_scores[dvr_a]["diff"] += diff_a
            round_scores[dvr_a]["n"] += 1

            round_scores[dvr_b]["diff"] += diff_b
            round_scores[dvr_b]["n"] += 1

            # store expected and final values
            exp += [e_a, e_b]
            out += [o_a, o_b]
        
        # insert score for end of round
        for dvr in round_scores.keys():
            if round_scores[dvr]["n"] != 0: # more than 1 car on grid
                elo_scores[dvr] += (round_scores[dvr]["diff"] / round_scores[dvr]["n"])
            
            cle_df.loc[valid_ix & (cle_df["driverId"] == dvr), "elo_score"] = elo_scores[dvr]

    if export == False:
        err_df = pd.DataFrame({"pred": exp, "true": out})
        err_df["squared_error"] = (err_df["true"] - err_df["pred"]) ** 2
        neg_sse = -err_df["squared_error"].sum()
    
        return neg_sse 
        # REPLACE WITH NDCG TO BEGIN BRINGING IN OTHER PARAMETERS, SSE FALLS OVER BRINGING IN POINTS 
        # SEE ONLY FOCUSSES ON ERROR OF E_A E_B VS OUTCOME
    
    else:
        cle_df.to_csv(f"{DATA_DIR}/interim/modelled_data.csv", index=False)


if __name__=="__main__":

    # find optimal parameters
    param_bounds = {
        "k": (1, 1000),
        "c": (1, 1000)
    }
    optimiser = bayes_opt.BayesianOptimization(
        f=model_data,
        pbounds=param_bounds,
        random_state=1,
        allow_duplicate_points=True
    )

    optimiser.maximize(init_points=20, n_iter=20)
    opt_results = optimiser.max
    opt_k = float(opt_results["params"]["k"])
    opt_c = float(opt_results["params"]["c"])
    opt_sse = float(-opt_results["target"])

    # log and print experiment outcome
    with dvclive.Live() as live:
        live.log_param("k", opt_k)
        live.log_param("c", opt_c)
        live.log_metric("SSE", opt_sse)

    print()
    print(opt_results)

    # create final model data
    model_data(k=opt_k, c=opt_c, export=True)

