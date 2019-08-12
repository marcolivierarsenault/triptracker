FROM python:3.7-alpine

EXPOSE 8050

WORKDIR /usr/src/app

RUN pip install --no-cache-dir dash boto3 gunicorn

COPY trip.py .
COPY assets ./assets

CMD [ "gunicorn", "-b", "0.0.0.0:8050", "trip:server" ]