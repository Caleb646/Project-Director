FROM python:3.9-slim-buster

COPY /backend/ /app/backend
COPY /docker/backend/dev/entrypoint.sh /docker/backend/entrypoint.sh

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /app/backend/project-director/requirements.txt

ENTRYPOINT [ "/docker/backend/entrypoint.sh" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"] #keeps the docker container terminal open