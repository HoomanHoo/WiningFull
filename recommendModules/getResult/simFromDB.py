import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from recommendModules.assistanceFunction.managingData import get_csv_from_db,\
    file_names
from recommendModules.assistanceFunction.dataConverter import csv_to_df,\
    df_to_csv

"""
sql[0] = "SELECT * FROM bit.win_wine"
sql[1] = "SELECT * FROM bit.win_wine_region"
sql[2] = "SELECT * FROM bit.win_user_grade"
sql[3] = "SELECT * FROM bit.win_user"
sql[4] = "SELECT * FROM bit.win_board"
sql[5] = "SELECT * FROM bit.win_board_img"
sql[6] = "SELECT * FROM bit.win_cart"
sql[7] = "SELECT * FROM bit.win_cart_detail"
sql[8] = "SELECT * FROM bit.win_comment"
sql[9] = "SELECT * FROM bit.win_detail_view"
sql[10] = "SELECT * FROM bit.win_detail_view_n"
sql[11] = "SELECT * FROM bit.win_point_his"
sql[12] = "SELECT * FROM bit.win_purchase"
sql[13] = "SELECT * FROM bit.win_purchase_detail"
sql[14] = "SELECT * FROM bit.win_receive_code"
sql[15] = "SELECT * FROM bit.win_revenue"
sql[16] = "SELECT * FROM bit.win_review"
sql[17] = "SELECT * FROM bit.win_search"
sql[18] = "SELECT * FROM bit.win_search_n"
sql[19] = "SELECT * FROM bit.win_sell"
sql[20] = "SELECT * FROM bit.win_store_excel"
sql[21] = "SELECT * FROM bit.win_store_url"
sql[22] = "SELECT * FROM bit.win_store"
sql[23] = "SELECT * FROM bit.win_user_favorite"
"""


def result_function(cart, purchase, review, detail, detail_n, weight_list):
    result = (cart * weight_list[0] + purchase * weight_list[1] + review * weight_list[2] + \
            detail * weight_list[3] + detail_n * weight_list[4]) / 100 
    return result


"""
cart.csv

sell 
sell_id, wine_id, sell_price

cart_detail 
cart_id, sell_id, cart_det_qnty

cart
cart_id, user_id

(cart_id, sell_id, cart_det_qnty) MERGE (cart_id, user_id)
=> (cart_id, user_id, sell_id, cart_det_qnty)

(cart_id, user_id, sell_id, cart_det_qnty) MERGE (sell_id, wine_id, sell_price)
=> (user_id, sell_id, cart_det_qnty, wine_id, sell_price)
=> (user_id, wine_id, f(cart_det_qnty, sell_price))

"""

def get_cart_matrix(dF_cart, dF_cart_detail, dF_sell, dF_wine_id, dF_user_id):
    
    cart_m1 = pd.merge(dF_cart, dF_cart_detail, on = 'cart_id', how = 'left')
    cart_m1 = cart_m1[["cart_id", "user_id", "sell_id", "cart_det_qnty"]]
    print(cart_m1)
    print(cart_m1.columns)
    print(cart_m1.shape)
    
    
    cart_m2 = pd.merge(cart_m1, dF_sell, on = 'sell_id', how = 'outer')
    #cart_m2 = cart_m2[["user_id", "wine_id", "cart_det_qnty", "sell_price"]]
    cart_m2 = cart_m2[["user_id", "wine_id", "cart_det_qnty"]]
    cart_m2 = cart_m2.dropna(axis=0)
    print(cart_m2)
    print(cart_m2.columns)
    print(cart_m2.shape)
    df_to_csv(cart_m2, "cart_m2")
    # cart_m2["factor"] = mini_test_function(cart_m2["cart_det_qnty"], cart_m2["sell_price"])
    # cart_result = cart_m2[["user_id", "wine_id", "factor"]]
    # print(cart_result)
    # print(cart_result.columns)
    # print(cart_result.shape)
    
    cart_m3 = pd.merge(cart_m2, dF_wine_id, on = 'wine_id', how = 'outer')
    df_to_csv(cart_m3, "cart_m3")
    cart_m3['cart_det_qnty'] = cart_m3['cart_det_qnty'].fillna(0)
    
    cart_m = pd.merge(cart_m3, dF_user_id, on = 'user_id', how = 'outer')
    cart_m['user_id'] = cart_m['user_id'].fillna("가상")
    df_to_csv(cart_m, "cart_merged")
    
    
    cart_matrix = pd.pivot_table(cart_m, values='cart_det_qnty', index=['user_id'],
                        columns=['wine_id'], fill_value=0, aggfunc=np.sum)
    cart_matrix.fillna( 0, inplace=True ) 
    if "가상" in cart_matrix.index.to_list():
        cart_matrix = cart_matrix.drop(index="가상")
    df_to_csv(cart_matrix, "cart_matrix_filled")
    
    return cart_matrix



    

"""
purchase.csv

sell 
sell_id, wine_id, sell_price

purchase_detail 
purchase_id, sell_id, purchase_det_number, purchase_detail_price

purchase
purchase_id, user_id

(sell_id, purchase_det_number, purchase_det_state) MERGE (purchase_id, user_id)
=> (purchase_id, user_id, sell_id, purchase_det_number, purchase_detail_price)

(purchase_id, user_id, sell_id, purchase_det_number, purchase_detail_price) MERGE (sell_id, wine_id, sell_price)
=> (user_id, wine_id, sell_id, purchase_det_number, purchase_detail_price)
=> (user_id, wine_id, f(purchase_det_number, purchase_detail_price))

"""


def get_puchase_matrix(dF_purchase, dF_purchase_detail, dF_sell, dF_wine_id, dF_user_id):
    purchase_m1 = pd.merge(dF_purchase, dF_purchase_detail, on = 'purchase_id', how = 'left')
    purchase_m1 = purchase_m1[["purchase_id", "user_id", "sell_id", "purchase_det_number", "purchase_det_price"]]
    print(purchase_m1)
    print(purchase_m1.columns)
    print(purchase_m1.shape)
    
    
    purchase_m2 = pd.merge(purchase_m1, dF_sell, on = 'sell_id', how = 'outer')
    # purchase_m2 = purchase_m2[["user_id", "wine_id", "purchase_det_number", "purchase_det_price"]]
    purchase_m2 = purchase_m2[["user_id", "wine_id", "purchase_det_number"]]
    purchase_m2 = purchase_m2.dropna(axis=0)
    print(purchase_m2)
    print(purchase_m2.columns)
    print(purchase_m2.shape)
    # purchase_m2["factor"] = mini_test_function(purchase_m2["cart_det_qnty"], purchase_m2["sell_price"])
    # purchase_result = purchase_m2[["user_id", "wine_id", "factor"]]
    # print(purchase_result)
    # print(purchase_result.columns)
    # print(purchase_result.shape)
    df_to_csv(purchase_m2, "purchase_m2")
    
    purchase_m3 = pd.merge(purchase_m2, dF_wine_id, on = 'wine_id', how = 'outer')
    purchase_m3['purchase_det_number'] = purchase_m3['purchase_det_number'].fillna(0)
    df_to_csv(purchase_m3, "purchase_m3")
    
    purchase_m = pd.merge(purchase_m3, dF_user_id, on = 'user_id', how = 'outer')
    purchase_m['user_id'] = purchase_m['user_id'].fillna("가상")
    df_to_csv(purchase_m, "purchase_merged")
    
    purchase_matrix = pd.pivot_table(purchase_m, values='purchase_det_number', index=['user_id'],
                        columns=['wine_id'], fill_value=0, aggfunc=np.sum)
    purchase_matrix.fillna( 0, inplace=True ) 
    if "가상" in purchase_matrix.index.to_list():
        purchase_matrix = purchase_matrix.drop(index="가상")
    df_to_csv(purchase_matrix, "purchase_matrix_filled")
    
    return purchase_matrix

"""
review.csv

sell 
sell_id, wine_id, sell_price

review 
user_id, sell_id, review_score

(sell_id, wine_id, sell_price) MERGE (user_id, sell_id, review_score)
=> (sell_id, user_id, wine_id, review_score)
=> (user_id, wine_id, review_score)

"""

def get_review_matrix(dF_review, dF_sell, dF_wine_id, dF_user_id):

    review_m1 = pd.merge(dF_review, dF_sell, on ='sell_id', how ='left')
    review_m1 = review_m1[["user_id", "wine_id", "review_score"]]
    print(review_m1)
    print(review_m1.columns)
    print(review_m1.shape)
    df_to_csv(review_m1, "review_m1")
    
    review_m2 = pd.merge(review_m1, dF_wine_id, on = 'wine_id', how = 'outer')
    review_m2['review_score'] = review_m2['review_score'].fillna(0)
    df_to_csv(review_m2, "review_m2")
    
    review_m = pd.merge(review_m2, dF_user_id, on = 'user_id', how = 'outer')
    review_m['user_id'] = review_m['user_id'].fillna("가상")
    df_to_csv(review_m, "review_merged")
    
    review_matrix = pd.pivot_table(review_m, values='review_score', index=['user_id'],
                        columns=['wine_id'], fill_value=0, aggfunc=np.mean)
    review_matrix.fillna( 0, inplace=True ) 
    if "가상" in review_matrix.index.to_list():
        review_matrix = review_matrix.drop(index="가상")
    df_to_csv(review_matrix, "review_matrix_filled")
    
    return review_matrix

"""
detail_view 
user_id, wine_id, detail_view_time

"""

def get_detail_matrix(dF_detail_view, dF_wine_id, dF_user_id):
    
    df_to_csv(dF_detail_view, "dF_detail_view")
    dF_detail_view = dF_detail_view.drop_duplicates(['detail_view_time'], keep = 'first')
    dF_detail_view = dF_detail_view[dF_detail_view["user_id"].isin(list(dF_user_id.iloc[:,0]))]
    dF_detail_view["count"] = 1
    dF_detail_view = dF_detail_view.groupby(["user_id", "wine_id"])["count"].count().reset_index()
    #df = df.groupby(['name','age','city'])['counter'].sum().reset_index()
    #dF_detail_view = dF_detail_view.
    print(dF_detail_view)
    print(dF_detail_view.columns)
    print(dF_detail_view.shape)
    df_to_csv(dF_detail_view, "detail_merged")
    
    dF_detail_view_m1 = pd.merge(dF_detail_view, dF_wine_id, on = 'wine_id', how = 'outer')
    dF_detail_view_m1['count'] = dF_detail_view_m1['count'].fillna(0)
    df_to_csv(dF_detail_view_m1, "dF_detail_view_m1")
    
    #dF_detail_view_m1['user_id']=dF_detail_view_m1['user_id'].astype(int)
    dF_detail_view_m = pd.merge(dF_detail_view_m1, dF_user_id, on = 'user_id', how = 'outer')
    dF_detail_view_m['user_id'] = dF_detail_view_m['user_id'].fillna("가상")
    df_to_csv(dF_detail_view_m, "dF_detail_view_merged")
    
    dF_detail_view_matrix = pd.pivot_table(dF_detail_view_m, values='count', index=['user_id'],
                        columns=['wine_id'], fill_value=0, aggfunc=np.sum)
    dF_detail_view_matrix.fillna( 0, inplace=True ) 
    if "가상" in dF_detail_view_matrix.index.to_list():
        dF_detail_view_matrix = dF_detail_view_matrix.drop(index="가상")
    df_to_csv(dF_detail_view_matrix, "dF_detail_view_matrix_filled")
    
    return dF_detail_view_matrix

"""
search
user_id, search_word, search_time 

"""
# print(dF_search)
# print(dF_search.columns)
# print(dF_search.shape)
# df_to_csv(dF_search, "search_merged")


"""
detail_view_n
wine_id, detail_view_n_time

"""
def get_detail_n_matrix(dF_detail_view_n, dF_wine_id, dF_user_id):

    dF_detail_view_n = dF_detail_view_n.drop_duplicates(['detail_view_n_time'], keep = 'first')
    dF_detail_view_n["count"] = 1
    dF_detail_view_n = dF_detail_view_n.groupby(["wine_id"])["count"].count().reset_index()
    print(dF_detail_view_n)
    print(dF_detail_view_n.columns)
    print(dF_detail_view_n.shape)
    df_to_csv(dF_detail_view_n, "detail_n_merged")
    
    dF_detail_view_n_m1 = pd.merge(dF_detail_view_n, dF_wine_id, on = 'wine_id', how = 'outer')
    dF_detail_view_n_m1['count'] = dF_detail_view_n_m1['count'].fillna(0)
    df_to_csv(dF_detail_view_n_m1, "dF_detail_view_n_m1")
    
    #dF_detail_view_n_m1['user_id']=dF_detail_view_n_m1['user_id'].astype(int)
    dF_detail_view_n_m = pd.concat([dF_detail_view_n_m1, dF_user_id], axis=1)
    dF_detail_view_n_m['user_id'] = dF_detail_view_n_m['user_id'].fillna("가상")
    df_to_csv(dF_detail_view_n_m, "dF_detail_view_n_merged")
    
    dF_detail_view_n_matrix = pd.pivot_table(dF_detail_view_n_m, values='count', index=['user_id'],
                        columns=['wine_id'], fill_value=0, aggfunc=np.mean)
    dF_detail_view_n_matrix.fillna( 0, inplace=True ) 
    if "가상" in dF_detail_view_n_matrix.index.to_list():
        dF_detail_view_n_matrix = dF_detail_view_n_matrix.drop(index="가상")
    for i in range(len(dF_detail_view_n_matrix)):
        dF_detail_view_n_matrix.iloc[i, :] = max(np.array(dF_detail_view_n_matrix.iloc[i, :]))
    print(dF_detail_view_n_matrix)
    df_to_csv(dF_detail_view_n_matrix, "dF_detail_view_n_matrix_filled")
    
    return dF_detail_view_n_matrix

"""
search_n
search_n_word, search_time 

"""
# print(dF_search_n)
# print(dF_search_n.columns)
# print(dF_search_n.shape)
# df_to_csv(dF_search_n, "search_n_merged")


def user_usage_qnty(user_id):
    cart_merged = csv_to_df("./csvStorage/csvFromDB/cart_merged.csv")
    purchase_merged = csv_to_df("./csvStorage/csvFromDB/purchase_merged.csv")
    review_merged = csv_to_df("./csvStorage/csvFromDB/review_merged.csv")
    detail_view_merged = csv_to_df("./csvStorage/csvFromDB/dF_detail_view_merged.csv")

    cart_usage = cart_merged.loc[cart_merged["user_id"] == user_id].shape[0]
    purchase_usage = purchase_merged.loc[purchase_merged["user_id"] == user_id].shape[0]
    review_usage = review_merged.loc[review_merged["user_id"] == user_id].shape[0]
    detail_usage = detail_view_merged.loc[detail_view_merged["user_id"] == user_id].shape[0]
    
    print(cart_usage)
    print(purchase_usage)
    print(review_usage)
    print(detail_usage)

    usage = cart_usage*5 + purchase_usage*10 + review_usage*20 + detail_usage*0.1
    
    if usage < 20 : 
        result = 0
    elif usage >= 20 and usage < 30 : 
        result = 10
    elif usage >= 30 and usage < 50 : 
        result = 30 
    elif usage >= 50 and usage < 100 : 
        result = 50 
    elif usage >= 100 and usage < 200 : 
        result = 70 
    elif usage >= 200 and usage < 500 : 
        result = 90 
    else : 
        result = 99 
        
    return result 



