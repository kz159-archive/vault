FROM python:3.8.2-alpine3.11
RUN apk update && apk add gcc build-base postgresql postgresql-dev
COPY requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . .
CMD python3 main.py
