FROM python:3.10-alpine

WORKDIR /mkv

COPY ./kvc /mkv/kvc
COPY main.py /mkv/main.py

RUN apk add gcc python3-dev build-base linux-headers
RUN python3 -m pip install psutil

ENV MKV_HOST=0.0.0.0

CMD ["python3", "main.py"]
