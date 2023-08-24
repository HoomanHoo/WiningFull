#!/usr/bin/bash

#echo $(python manage.py migrate detail)
#echo $(python manage.py migrate user)
#echo $(python manage.py migrate board)
#echo $(python manage.py migrate purchasing)
#echo $(python manage.py migrate search)
#echo $(python manage.py migrate store)
#echo $(python manage.py makemigrations)
#echo $(python manage.py migrate)
echo $(gunicorn Wining.wsgi:application --bind 0.0.0.0:8001)
echo "gunicorn Wining.wsgi:application --bind 0.0.0.0:8001"













