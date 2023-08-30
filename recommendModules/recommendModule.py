

"""

# Wining Recommend에서 onclick 실행

# DB 기반 CSV 파일을 DatrFrame으로 불러온다. 
# logging 기반 CSV 파일을 데이터를 DataFrame으로 불러온다.

# user 의 회원 정보 입력 기반으로 user_favorite과 wine 의 유사도를 pivot 한다. (1)


# 각 DataFrame마다
# user_id 와 wine_id와 다른 컬럼을 남겨서 user_id 기준으로 pivot 한다. 

# pivot 결과 간의 연산을 적용한다. (2)

# user 의 사용 누적 정도를 측정한다. 
# 사용 누적 정도에 따라 가중치를 달리 하여 (1) 과 (2) 를 합산한다. 


# 코사인 유사도 적용 


# 중복 제외 처리 

"""
import pandas as pd

from recommendModules.assistanceFunction.dataConverter import df_to_csv,\
    csv_to_df, df_to_db

from recommendModules.assistanceFunction.managingData import get_csv_from_db,\
    file_names
from sklearn.metrics.pairwise import cosine_similarity
from recommendModules.getResult.simFromDB import get_cart_matrix,\
    get_puchase_matrix, get_review_matrix, get_detail_matrix,\
    get_detail_n_matrix, result_function
from recommendModules.getResult.simFromFav import get_user_similarity
import operator
from _datetime import datetime
from sqlalchemy.engine.create import create_engine
import pymysql
from pymysql.constants import CLIENT


# DB의 테이블들을 DataFrame으로 변환해두고 CSV파일로 저장한다.
df_list_from_db = []
req_list = [0, 3, 6, 7, 9, 10, 12, 13, 16, 17, 18, 19, 23]
get_csv_from_db(req_list)
for i in range(len(req_list)):
    print(file_names[req_list[i]])
    df = csv_to_df("./csvStorage/csvFromDB/"+ file_names[req_list[i]] + ".csv")
    df_list_from_db.append(df)

dF_wine = df_list_from_db[0]
dF_user = df_list_from_db[1]
dF_cart = df_list_from_db[2]
dF_cart_detail = df_list_from_db[3]
dF_detail_view = df_list_from_db[4]
dF_detail_view_n = df_list_from_db[5]
dF_purchase = df_list_from_db[6]
dF_purchase_detail = df_list_from_db[7]
dF_review = df_list_from_db[8]
dF_search = df_list_from_db[9]
dF_search_n = df_list_from_db[10]
dF_sell = df_list_from_db[11]
dF_user_fav = df_list_from_db[12]


# DB에서 와인 데이터를 불러 DataFrame 으로 만든다.
# get_csv_from_db([0])
# dF_wine = csv_to_df("./csvStorage/csvFromDB/win_wine.csv")
print(dF_wine)
print(dF_wine.shape)
print(dF_wine.columns)

# 일반유저의 id를 따로 분리
dF_user_gen = dF_user[dF_user["user_grade"]==1]
print(dF_user_gen.shape)
dF_user_id = dF_user_gen[["user_id"]]
print(dF_user_id.shape)

# 와인 아이디 따로 분리
dF_wine_id = dF_wine[["wine_id"]]
print(dF_wine_id.shape)


df_to_csv(dF_wine_id, "dF_wine_id")
df_to_csv(dF_user_id, "dF_user_id")


# DB에서 win_user_favorite 을 불러 DataFrame 으로 만든다. 
# get_csv_from_db([23])
# dF_user_fav = csv_to_df("./csvStorage/csvFromDB/win_user_favorite.csv")
print(dF_user_fav.shape)


# 회원 수정 이력이 있는 user는 현재 상태만 남긴다. 
dF_user_fav = dF_user_fav.drop_duplicates(['user_id'], keep = 'last')
print(dF_user_fav)
print(dF_user_fav.shape)
print(dF_user_fav.columns)

print(len(dF_wine))
print(len(dF_user_fav))


# 회원 정보 입력 기반 DataFrame 

dF_fav_result = get_user_similarity(dF_user_fav, dF_wine)
print(list(dF_wine_id.iloc[:,0]))
print(list(dF_user_id.iloc[:,0]))
dF_fav_result.index = dF_wine_id.iloc[:,0].tolist()
dF_fav_result.columns = dF_user_id.iloc[:,0].tolist()


print(dF_fav_result)
print(dF_fav_result.shape)
df_to_csv(dF_fav_result, "data_from_user_fav_input")






cart_matrix = get_cart_matrix(dF_cart, dF_cart_detail, dF_sell, dF_wine_id, dF_user_id)
purchase_matrix = get_puchase_matrix(dF_purchase, dF_purchase_detail, dF_sell, dF_wine_id, dF_user_id)
review_matrix = get_review_matrix(dF_review, dF_sell, dF_wine_id, dF_user_id)
dF_detail_view_matrix = get_detail_matrix(dF_detail_view, dF_wine_id, dF_user_id)
dF_detail_view_n_matrix = get_detail_n_matrix(dF_detail_view_n, dF_wine_id, dF_user_id)

dF_user_and_wine = pd.merge(dF_purchase, dF_purchase_detail, on = 'purchase_id', how = 'outer')

print(cart_matrix.shape)
print(purchase_matrix.shape)
print(review_matrix.shape)
print(dF_detail_view_matrix.shape)
print(dF_detail_view_n_matrix.shape)

dF_db_result = result_function(cart_matrix, purchase_matrix, review_matrix, dF_detail_view_matrix, dF_detail_view_n_matrix, [10, 30, 100, 5, 0.1])
dF_db_result = dF_db_result.T.fillna(0)
print(dF_db_result)
print(dF_db_result.columns)
print(dF_db_result.shape)
df_to_csv(dF_db_result, "data_from_db")





dF_result = dF_fav_result + dF_db_result
print(dF_result)
print(dF_result.columns)
print(dF_result.shape)
df_to_csv(dF_db_result, "dF_db_result")
df_to_csv(dF_result, "dF_result")


item_matrix = dF_result
user_matrix = dF_result.T


# item_similarity = cosine_similarity( dF_result )         # 아이템 기반
# user_similarity = cosine_similarity( dF_result.T )       # 사용자 기반 
# item_similarity    = pd.DataFrame(item_similarity)
# user_similarity    = pd.DataFrame(user_similarity)     
# print( item_similarity )                             
# print( user_similarity )                              
#
# df_to_csv(item_similarity, "item_similarity")
# df_to_csv(user_similarity, "user_similarity")


def similar_users_func(user_id, matrix, k):
    # 현재 유저에 대한 데이터프레임 만들기
    # matrix의 index = user_id -> 현재 1명 유저에 대한 평가 정보 찾기
    user = matrix[matrix.index == user_id]
    print(user.shape)
    # matrix index 값이 user_id와 다른가?
    # 일치하지 않는 값들은 other_users
    other_users = matrix[matrix.index != user_id]
    print(other_users.shape)
    # 대상 user, 다른 유저와의 cosine 유사도 계산 
    # list 변환
    similarities = cosine_similarity(user,other_users)[0].tolist()
    print(similarities)
    # 다른 사용자의 인덱스 목록 생성
    other_users_list = other_users.index.tolist()
    print(other_users_list)
    
    # 인덱스/유사도로 이뤄진 딕셔너리 생성
    # dict(zip()) -> {'other_users_list1': similarities, 'other_users_list2': similarities}
    user_similarity = dict(zip(other_users_list, similarities))
    
    # 딕셔너리 정렬
    # key=operator.itemgetter(1) -> 오름차순 정렬 -> reverse -> 내림차순
    user_similarity_sorted = sorted(user_similarity.items(), key=operator.itemgetter(1))
    user_similarity_sorted.reverse()
    
    # 가장 높은 유사도 k개 정렬하기
    top_users_similarities = user_similarity_sorted[:k]
    users = [i[0] for i in top_users_similarities]
    
    return users
    # 현재 유저에 대한 정보 찾기





def recommend_item_func(user_index, similar_user_indices, matrix, purchase_filter, items=10):
    # 유저와 비슷한 유저 가져오기
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    print(similar_users)
    # 비슷한 유저 평균 계산 # row 계산
    similar_users = similar_users.mean(axis=0)
    # dataframe 변환 : 정렬/필터링 용이
    similar_users_df = pd.DataFrame(similar_users, columns=['user_similarity'])
    print(similar_users_df)
    # 현재 사용자의 벡터 가져오기 : matrix = rating_matrix(pivot table)
    user_df = matrix[matrix.index == user_index]
    print(user_df)
    # 현재 사용자의 평가 데이터 정렬
    user_df_transposed = user_df.transpose()
    print(user_df_transposed)
    # 컬럼명 변경 48432 -> rating
    user_df_transposed.columns = ['rating']
    print(user_df_transposed)
    # 미시청 콘텐츠는 rating 0로 바꾸어 준다. remove any rows without a 0 value. Anime not watched yet
    #user_df_transposed = user_df_transposed[user_df_transposed['rating']==0]
    
    # 미시청 콘텐츠 목록리스트 만들기
    wines_not_purchased = user_df_transposed.index.tolist()
    print(wines_not_purchased)
    # 안본 콘텐츠 필터링
    similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(wines_not_purchased)]
    print(similar_users_df_filtered)
    # 평균값을 기준으로 내림차순 정렬
    similar_users_df_ordered = similar_users_df_filtered.sort_values(by=['user_similarity'], ascending=False)
    print(similar_users_df_ordered)
    # 상위 10개 값 가져오기
    # items = 10
    similar_users_df_ordered = similar_users_df_ordered[similar_users_df_ordered.index.isin(purchase_filter)]
    top_n_wines = similar_users_df_ordered.head(items)
    top_n_wines_indices = top_n_wines.index.tolist()

    # anime dataframe에서 top10값 찾기
    wines_information = dF_wine_id[dF_wine_id["wine_id"].isin(top_n_wines_indices)]
    
    return wines_information #items

print(dF_user_id)
dF_gen_id = dF_user_id["user_id"].tolist()
print(dF_gen_id)
print(len(dF_gen_id))



print("반복문 시작")

recommend_table = []
for idx in range(len(dF_gen_id)):
    
    print(dF_gen_id[idx])
    similar_users = similar_users_func(dF_gen_id[idx], user_matrix, 10)
    print(similar_users)
    print(purchase_matrix.T)
    print( purchase_matrix.T[dF_gen_id[idx]])
    purchase_filter_idx = purchase_matrix.T[dF_gen_id[idx]].index.tolist()
    print(purchase_filter_idx)
    purchase_filter_purchase = purchase_matrix.T[dF_gen_id[idx]].tolist()
    print(purchase_filter_purchase)
    purchase_filter = []
    for i in range(len(purchase_filter_idx)):
        if purchase_filter_purchase[i]==0:
            purchase_filter.append(purchase_filter_idx[i])
    print(purchase_filter)
    print("purchase_filter")
    print(purchase_filter_idx)
    print(purchase_filter_purchase)
    print(purchase_filter)
    print(len(purchase_filter))
      
        # 추천 콘텐츠 뽑아내기
    recommend_content = recommend_item_func(dF_gen_id[idx], similar_users, user_matrix, purchase_filter)
    
    print(dF_gen_id[idx])
    print(recommend_content)
    recommend_table.append(recommend_content.index.tolist())

recommend_table = pd.DataFrame(recommend_table)
print(recommend_table)
print(recommend_table.shape)
# 모든 추천




user_db = pymysql.connect(
    user = 'bit',
        password = 'bit',
        host = '127.0.0.1', 
        db = 'bit',
        charset = 'utf8',
        client_flag= CLIENT.MULTI_STATEMENTS
      )
# cursor 설정
cursor = user_db.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT MAX(recommend_id) FROM win_recommend")
max_id = cursor.fetchall()





list_rec_id = range(1, len(dF_gen_id)+1)
print(list_rec_id)
print(dF_gen_id)
#lc_time = time.localtime() 
#t = time.strftime("%Y-%m-%d %H:%M:%S", lc_time)
t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
list_reg_time = [t] * len(dF_gen_id)
print(list_reg_time)
print(len(list_reg_time))

recommend_table.insert(0, "recommend_id", list_rec_id)
recommend_table.insert(1, "user_id", dF_gen_id)
recommend_table.insert(12, "update_time", list_reg_time)


recommend_table.columns=["recommend_id", "user_id", "recommend_rank_1", "recommend_rank_2", "recommend_rank_3", "recommend_rank_4", "recommend_rank_5", 
                                                   "recommend_rank_6", "recommend_rank_7", "recommend_rank_8", "recommend_rank_9", "recommend_rank_10", "update_time"]
print(recommend_table)

df_to_csv(recommend_table, "recommend_table")



df_to_db(recommend_table, "win_recommend")



