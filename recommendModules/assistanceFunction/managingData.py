import pymysql
import pandas as pd
import os
from os import path

# DB 연결
user_db = pymysql.connect(
        user = 'bit',
            password = 'bit',
            host = '127.0.0.1',
            db = 'bit',
            charset = 'utf8'
          )
# cursor 설정
cursor = user_db.cursor(pymysql.cursors.DictCursor)

sql = [0 for i in range(24)]

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

file_names = ["win_wine", "win_wine_region", "win_user_grade", "win_user", "win_board", "win_board_img", "win_cart", "cart_detail",
               "win_comment", "win_detail_view", "win_detail_view_n", "win_point_his", "win_purchase", "win_purchase_detail", 
               "win_receive_code", "win_revenue", "win_review","win_search", "win_search_n", "win_sell", "win_store_excel", 
               "win_store_url", "win_store", "win_user_favorite"]

# 결과를 pandas 데이터프레임으로 변환

  
# files = pd.read_csv( "./name.csv" ) 
# print(files)


def get_csv_from_db (list) : 
    for i in range(len(list)) :
        print(file_names[list[i]])
        cursor.execute(sql[list[i]])
        result = cursor.fetchall()
        #file_name = "./table_" + str(list[i]) + ".csv"
        file_name = "./csvStorage/csvFromDB/" + file_names[list[i]] + ".csv"
        result = pd.DataFrame(result)
        if path.exists(file_name) == True :
            os.remove(file_name)
            result.to_csv(file_name, index = False)
        else :
            result.to_csv(file_name, index = False)
            
    

        