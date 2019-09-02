FROM python:3.7.4-alpine3.10

RUN mkdir /app
WORKDIR /app
ADD . /app/
# Depedendicas paramiko
RUN apk add py-pip python-dev libffi-dev openssl-dev gcc libc-dev make
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/server.py"]