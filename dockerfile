FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /project/
ADD . /project/

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python manage.py makemigrations
