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


def fib(n):
    a, b = 1, 0
    if n == 0:
        return 0
    if n == 1:
        return 1
    for _ in range(1, n):
        a, b = a+b, a
    return a


def send():
    # establish connection
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = conn.channel()

    # declare exchange name&type
    chan.exchange_declare(exchange='topic_logs', exchange_type='topic')
    # declare message_queue name
    # chan.queue_declare(message_queue='leo')

    # declare a routing_key(message_queue name)
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    # publish a message
    message = ''.join(sys.argv[2:] or 'Hello RabbitMQ')
    # when declare exchange,need named exchange, do not declare routing_key(means message_queue name)

    chan.basic_publish(exchange='topic_logs',
                       routing_key=routing_key,
                       body=message,
                       # message persistent
                       # properties=pika.BasicProperties(delivery_mode=2)
                       )

    print('[Sender] Sent message {}'.format(message))
    # gently close the connection
    chan.close()


if __name__ == '__main__':
    send()
