#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.20.10.106',30672,'/',credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters('10.43.161.101',31672))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
	if 'true' in body:
		print("True")
	else:
		print("False")
    # print(" [x] Received %r" % body)

# channel.basic_consume(callback,queue='hello',no_ack=True)
channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
