FROM python:3.7-alpine

EXPOSE 8050

WORKDIR /usr/src/app

RUN pip install --no-cache-dir dash boto3

COPY trip.py .

CMD [ "python", "./trip.py" ]