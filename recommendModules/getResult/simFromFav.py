import numpy as np
import pandas as pd
from recommendModules.assistanceFunction.dataConverter import csv_to_df,\
    df_to_csv
from recommendModules.assistanceFunction.managingData import get_csv_from_db
from recommendModules.assistanceFunction.functions import win_reco_color,\
    win_reco_alc, win_corr_alc_inverse, win_reco_taste, win_reco_food




def get_user_similarity(df_user_fav, df_wine):
    
    df_result = pd.DataFrame()
    
    plane=[]
    
    for idx_wine in range(len(df_wine)):
        
        row = []
        
        for idx_user_fav in range(len(df_user_fav)):
            
            user_favorite = [
            df_user_fav.loc[idx_user_fav, "fav_wine_color"],
            df_user_fav.loc[idx_user_fav, "fav_alc"],
            df_user_fav.loc[idx_user_fav, "fav_sweet"], 
            df_user_fav.loc[idx_user_fav, "fav_bitter"],
            df_user_fav.loc[idx_user_fav, "fav_sour"],
            df_user_fav.loc[idx_user_fav, "fav_food"]
        ]
            # 우선순위별 가중치 점수 부여하기
            arr = [0.05]
            user_prior = arr * 6
            user_prior[df_user_fav.loc[idx_user_fav, "fav_first_priority"] - 1] += 0.45
            user_prior[df_user_fav.loc[idx_user_fav, "fav_second_priority"] - 1] += 0.20
            user_prior[df_user_fav.loc[idx_user_fav, "fav_third_priority"] - 1] += 0.05
            # 50 25 10 5 5 5 

            # 회원 취향과 와인 특성 매칭해서 각 항목별 점수 얻기
            color_score = win_reco_color(user_favorite[0], df_wine.loc[idx_wine, "wine_sort"])
            alc_score = win_reco_alc(
                user_favorite[1], win_corr_alc_inverse(df_wine.loc[idx_wine, "wine_alc"])
            )
            sweet_score = win_reco_taste(user_favorite[2], df_wine.loc[idx_wine, "wine_dangdo"])
            bitter_score = win_reco_taste(user_favorite[3], df_wine.loc[idx_wine, "wine_tannin"])
            sour_score = win_reco_taste(user_favorite[4], df_wine.loc[idx_wine, "wine_sando"])
            food_score = win_reco_food(user_favorite[5], df_wine.loc[idx_wine, "wine_food"])
            
            user_similarity = (
                color_score * user_prior[0]
                + alc_score * user_prior[1]
                + sweet_score * user_prior[2]
                + bitter_score * user_prior[3]
                + sour_score * user_prior[4]
                + food_score * user_prior[5]
            )
            
            #df_result.loc[idx_wine, idx_user_fav] = user_similarity
            
            row.append(user_similarity)
        
        plane.append(row)
    
    df_result = pd.DataFrame(plane)
        
    return df_result 






