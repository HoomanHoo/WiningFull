FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /project/
ADD . /project/
COPY migrate.sh /migrate.sh
RUN chmod +x /migrate.sh
COPY save.sql /save.sql
RUN chmod +x /save.sql

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

