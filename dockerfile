FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-pip && apt-get -y install curl && apt-get -y install default-libmysqlclient-dev && apt-get -y install wget && apt-get install -y default-mysql-client && apt-get clean

WORKDIR /project/
ADD . /project/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY migrate.sh /migrate.sh
COPY save.sql /save.sql
COPY entrypoint.sh /entrypoint.sh
COPY pymysqlex.py /pymysqlex.py
RUN chmod +x /migrate.sh && chmod +x /save.sql && chmod +x /entrypoint.sh && chmod +x /pymysqlex.py
