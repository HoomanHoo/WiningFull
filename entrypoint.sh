#!/usr/bin/bash

# until (curl -v http://mysql:3307/); do
#     echo "mysql is still set up"
#     sleep 20
# done
sleep 360
echo "mysql is ready"

echo $(python manage.py makemigrations)
echo "python manage.py makemigrations"
echo $(python manage.py migrate)
echo "python manage.py migrate"

#echo $(python manage.py makemigrations detail)
#echo "python manage.py makemigrations detail"
#echo $(python manage.py makemigrations user)
#echo "python manage.py makemigrations user"
#echo $(python manage.py makemigrations board)
#echo "python manage.py makemigrations board"
#echo $(python manage.py makemigrations purchasing)
#echo "python manage.py makemigrations purchasing"
#echo $(python manage.py makemigrations search)
#echo "python manage.py makemigrations search"
#echo $(python manage.py makemigrations store)
#echo "python manage.py makemigrations store"
#echo $(python manage.py migrate detail)
#echo "python manage.py migrate detail"
#echo $(python manage.py migrate user)
#echo "python manage.py migrate user"
#echo $(python manage.py migrate board)
#echo "python manage.py migrate board"
#echo $(python manage.py migrate purchasing)
#echo "python manage.py migrate purchasing"
#echo $(python manage.py migrate search)
#echo "python manage.py migrate search"
#echo $(python manage.py migrate store)
#echo "python manage.py migrate store"
#echo $(python manage.py clearsessions)
#echo "python manage.py clearsessions"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'winingmailservice@naver.com', 'admin1234')" | python manage.py shell
echo "create admin"
echo $(gunicorn Wining.wsgi:application --bind 0.0.0.0:8001)
echo "gunicorn Wining.wsgi:application --bind 0.0.0.0:8001"


