# -*- coding: utf-8 -*-
"""
1. Install rabbitmq:
    brew install rabiitmq

2. Install pika
    pipenv install pika

3. Start rabbitmq server
     brew services start rabbitmq/rabbitmq-server(add the path first)
"""
import pika
import sys


def send():
    # establish connection
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = conn.channel()

    # declare queue name
    chan.queue_declare(queue='leo')

    # publish a message
    message = ''.join(sys.argv[1:] or 'Hello RabbitMQ')
    chan.basic_publish(exchange='',
                       routing_key='leo',
                       body=message,
                       # message persistent
                       properties=pika.BasicProperties(delivery_mode=2))

    print('[Sender] Sent message {}'.format(message))
    # gently close the connection
    chan.close()


if __name__ == '__main__':
    send()
