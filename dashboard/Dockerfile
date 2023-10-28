FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r ./requirements.txt
COPY ./dashboard ./dashboard
COPY ./wait-for.sh /usr/local/bin/wait-for.sh
RUN chmod +x /usr/local/bin/wait-for.sh

