FROM python:3.10-buster as base-py

WORKDIR /app
COPY ./requirements.txt /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY . .

EXPOSE 8000