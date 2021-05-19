FROM python:3

WORKDIR /usr/src/app

COPY entrypoint.sh .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .