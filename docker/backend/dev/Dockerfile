FROM python:3.9-slim-buster
#FROM python:3.10.1-buster

WORKDIR /app

COPY /backend/project-director/ /app/
COPY /docker/backend/dev/ /app/backend/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

#RUN apt-get update && apt-get install --yes postgresql-dev gcc python3-dev musl-dev libffi-dev
#RUN apt-get -qq update
#RUN apt-get install --yes httpd
#RUN apt-get install --yes apache2 apache2-dev
#RUN apt-get install --yes apache2 apache2-dev

#need gcc for uwsgi
RUN apt-get update && apt-get install --yes gcc 
RUN pip install -r ./requirements.txt
RUN pip install uwsgi

# ENTRYPOINT [ "entrypoint.dev.sh" ]
# CMD uwsgi --http "0.0.0.0:8000" --module project-director.wsgi --master --processes 4 --threads 2