FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /project/
ADD . /project/
COPY migrate.sh /migrate.sh
RUN chmod +x /migrate.sh

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python manage.py makemigrations detail
RUN python manage.py makemigrations user
RUN python manage.py makemigrations board
RUN python manage.py makemigrations purchasing
RUN python manage.py makemigrations search
RUN python manage.py makemigrations store
