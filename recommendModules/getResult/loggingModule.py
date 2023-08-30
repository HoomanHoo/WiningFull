import numpy as np 
import pandas as pd
#from search.functionsAndModules.functions import list_string_to_real
import re

"""
log파일 불러오기
빈 numpy.array 선언
로그 파일 줄 단위로 INFO 포함된 것만 array에 append
파일 닫기

View 클래스별로 분류
column 구분자 import
각 클래스별로 list 더해서 DataFrame 생성
DataFrame Merge 
"""



#f = open("logfile.log", "r", encoding='UTF8')
f = open("../../log/logfile.log", "r", encoding='UTF8')
# 로그파일을 열어서 읽습니다.

log_data = np.array([])
# 빠른 연산속도를 위해 로그파일을 저장할 리스트를 numpy.array 타입으로 생성을 합니다.

while True:
    line = f.readline()
    if not line:break
    
    if "INFO" in line:
        print(line, end="")
        log_data = np.append(log_data, line)
f.close
# 한 줄 단위로 log_data에 append합니다. line이 더 이상 존재하지 않으면 while문에서 벗어납니다.
# 저희 서비스의 logging_data 에는 INFO, WARNING, ERROR 세 종류의 로깅 데이터가 있습니다. 
# 이 중에서 INFO 데이터만 머신러닝에 사용을 하기 때문에 INFO에 해당하는 데이터만 array에 저장을 합니다.


print(log_data)
print(len(log_data))

print(log_data[278])


# str_list = "[1, 2, 3, None, 5]"
# real_list = list_string_to_real(str_list)



string_log = log_data[-100]
print(string_log)


p = re.compile('(?<=\[)(.*?)(?=\])')
result = p.findall(string_log)
result_2 = p.search(string_log)
print(result[0])


