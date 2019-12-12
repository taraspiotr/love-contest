FROM python:3.6.8-alpine

LABEL image for a 006 love contest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ARG FLASK_APP
ARG MYSQL_URI
ARG SECRET_KEY
ARG FLASK_CONFIG

RUN flask db upgrade 

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]