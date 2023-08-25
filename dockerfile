FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-pip && apt-get -y install curl && apt-get -y install default-libmysqlclient-dev && apt-get install wget && apt-get clean

WORKDIR /project/
ADD . /project/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY migrate.sh /migrate.sh
COPY bit_save.sql /bit_save.sql
COPY entrypoint.sh /entrypoint.sh
COPY entrypoint-db.sh /entrypoint-db.sh
RUN chmod +x /migrate.sh && chmod +x /bit_save.sql && chmod +x /entrypoint.sh && chmod +x /entrypoint-db.sh
