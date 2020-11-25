FROM python:3.7-slim

COPY Pipfile* /
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 5000

CMD ["python", "client.py", "--host=0.0.0.0"]