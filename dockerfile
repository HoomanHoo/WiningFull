# syntax = docker/dockerfile:1.2
#Dockerfile

From python:3.8
WORKDIR /user/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "unix:/run/gunicorn.sock", "Wining.wsgi:application"]
