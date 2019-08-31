FROM python:3.7.4-alpine3.10

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

COPY nginx-deployment.yaml /app/

EXPOSE 5000
CMD ["python", "/app/server.py"]