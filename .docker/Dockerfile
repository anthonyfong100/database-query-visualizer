FROM python:3.7-slim

COPY Pipfile* /
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get -q update && apt-get -qy install netcat


COPY . /app
COPY ./.docker/start.sh /start.sh

WORKDIR /app
EXPOSE 5000

CMD ["/start.sh"]