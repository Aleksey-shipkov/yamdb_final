FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY api_yamdb/ ./

CMD cd .. && gunicorn --bind 0.0.0.0:8000 yamdb_final.wsgi:application

