import pymysql

db = pymysql.connect(host="mysql", port=3307, user="bit", passwd="bit", db="bit", charset="utf8")
cusor = db.cursor()
sql = "select count(*) from win_user"
result = cusor.execute(sql)
print(result)