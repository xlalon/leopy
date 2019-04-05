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

    # declare exchange name&type
    chan.exchange_declare(exchange='direct_logs', exchange_type='direct')
    # declare queue name
    # chan.queue_declare(queue='leo')

    # declare a routing_key(queue name)
    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    # publish a message
    message = ''.join(sys.argv[2:] or 'Hello RabbitMQ')
    # when declare exchange,need named exchange, do not declare routing_key(means queue name)

    chan.basic_publish(exchange='direct_logs',
                       routing_key=severity,
                       body=message,
                       # message persistent
                       # properties=pika.BasicProperties(delivery_mode=2)
                       )

    print('[Sender] Sent message {}'.format(message))
    # gently close the connection
    chan.close()


if __name__ == '__main__':
    send()
