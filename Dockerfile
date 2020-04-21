FROM python:3.7-alpine3.9 as base

RUN apk update && apk add libffi libffi-dev postgresql-dev gcc g++ python3-dev musl-dev git
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt --user

WORKDIR /app
COPY proxies_vault /app

CMD ["python", "main.py"]
