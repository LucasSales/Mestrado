#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2',5672,'/',credentials))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
# channel.basic_publish(exchange='',routing_key='hello',body='true')

print(" [x] Sent 'Hello World!'")
connection.close()