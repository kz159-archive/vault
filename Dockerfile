FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install

RUN apk update && apk upgrade && \
    apk add bash git openssh postgresql-dev gcc python3-dev musl-dev libffi libffi-dev

WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local

RUN apk --no-cache add libpq
COPY proxies_vault ./

CMD ["python", "main.py"]
