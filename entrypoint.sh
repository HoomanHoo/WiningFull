#!/usr/bin/bash

while ! wget mysql:3307 ; do
    echo "mysql is still set up"
    sleep 15
done
#sleep 360
echo "mysql is ready"

result=$(mysql -hmysql -P3307 -uroot -pbit bit -e "select count(*) from auth_user")
echo ${result}
str=${result:9}
echo ${result}
echo ${str}

if [ ${str} -gt 0 ]; then
	echo "no migrate"
else
	echo "migrate start"
	echo $(python manage.py makemigrations)
	echo "python manage.py makemigrations"
	echo $(python manage.py migrate)
	echo "python manage.py migrate"
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'winingmailservice@naver.com', 'admin1234')" | python manage.py shell
	echo "create admin"
fi
echo $(gunicorn Wining.wsgi:application --bind 0.0.0.0:8001)
echo "gunicorn Wining.wsgi:application --bind 0.0.0.0:8001"


