FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-pip && apt-get -y install curl && apt-get -y install default-libmysqlclient-dev && apt-get -y install wget && apt-get install -y default-mysql-client && apt-get install -y vim && apt-get clean

WORKDIR /project/
ADD . /project/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## COPY save.sql /save.sql chmod +x /save.sql 

COPY entrypoint.sh /entrypoint.sh
RUN  chmod +x /entrypoint.sh
