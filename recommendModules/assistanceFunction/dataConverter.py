import pymysql
import pandas as pd
import os
from os import path
from sqlalchemy import create_engine

"""
DB, CSV, DataFrame 사이의 형식을 변환하기 위한 함수가 내장된 모듈입니다.
"""

# DB to DataFrame

def db_to_df(table_name):
    # MySQL 서버에 연결
    conn = pymysql.connect(
        host='127.0.0.1',
        user='bit',
        password='bit',
        db='bit',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )
    try:
        # 커서 생성
        with conn.cursor() as cursor:
        # 레코드 조회 쿼리 실행
            select_query = 'SELECT * FROM `' + table_name + '`;'
            cursor.execute(select_query)
            result = cursor.fetchall()
        # 조회 결과를 DataFrame으로 변환
        df = pd.DataFrame(result)
        # DataFrame 출력
    finally:
        # 연결 닫기
        conn.close()
    
    return df

# DB to CSV

def db_to_csv(table_name):
    result = db_to_df(table_name)
    file_name = "./csvStorage/csvFromDB/table_" + table_name + ".csv"
    
    if path.exists(file_name) == True :
        os.remove(file_name)
        result.to_csv(file_name, index = False)
    else :
        result.to_csv(file_name, index = False)


#db_to_csv("win_sell")

# DataFrame to DB

def df_to_db(df_name, table_name):
    engine = create_engine("mysql+pymysql://bit:bit@127.0.0.1/bit?charset=utf8mb4")
    conn = engine.connect()
    df_name.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    conn.close() 
    
# CSV to DB

# DataFrame to CSV

def df_to_csv(df_name, file_name):
    file_path = "./csvStorage/csvFromDB/" + file_name + ".csv"
    
    if path.exists(file_path) == True :
        os.remove(file_path)
        df_name.to_csv(file_path, index = False)
    else :
        df_name.to_csv(file_path, index = False)
       
#df_to_csv(df_test)
    

# CSV to DataFrame 

def csv_to_df(csv_path):
    
    df = pd.read_csv( csv_path ) 
    return df
    




