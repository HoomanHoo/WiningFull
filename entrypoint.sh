#!/usr/bin/bash

while ! wget mysql:3307 ; do
    echo "mysql is still set up"
    	sleep 15
done

echo "mysql is ready"
# docker mysql image를 사용할 시 해당 이미지가 실행되는 컨테이너의 상태를 파악한다

# while ! wget 192.168.0.3:3306 ; do
# wget container name or ip, endpoint:port number
#     echo "mysql is still set up"
    #     sleep 15
# done
# #sleep 360
# echo "mysql is ready"
# 가상머신 호스트 PC의 Mysql을 사용할 시 해당 서버와의 연결 상태를 확인한다

echo "Verify that there are existing superuser"
# result=$(mysql -h 192.168.0.3 -P3306 -ubit -pbit bit -e "select count(*) from auth_user") 
# 호스트 PC의 Mysql에 해당하는 테이블이 있는지, 슈퍼유저가 존재하는지 질의

#result=$(mysql -h sample-db.cuy0rgqhle4s.ap-northeast-2.rds.amazonaws.com -P3306 -ubit -pbit bit -e "select count(*) from auth_user")
# AWS RDS에 해당하는 테이블이 있는지, 슈퍼유저가 존재하는지 질의

result=$(mysql -hmysql -P3307 -uroot -pbit bit -e "select count(*) from auth_user")
# docker mysql container에 해당하는 테이블이 있는지, 슈퍼유저가 존재하는지 질의 

echo ${result}
str=${result:9}
echo ${str}

if [ ${str} -gt 0 ]; then
	echo "no migrate"
else
	echo "migrate start"
	echo "python manage.py makemigrations"
	echo $(python manage.py makemigrations)
	echo "python manage.py migrate"
	echo $(python manage.py migrate)
	echo "create admin"
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'winingmailservice@naver.com', 'admin1234')" | python manage.py shell
	
fi
echo "gunicorn Wining.wsgi:application --bind 0.0.0.0:8001"
echo $(gunicorn Wining.wsgi:application --bind 0.0.0.0:8001)


