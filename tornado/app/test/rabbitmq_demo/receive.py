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
import time


def receive():
    # establish connection
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = conn.channel()

    # declare queue name
    chan.queue_declare(queue='leo')

    #  don't dispatch a new message to a worker until it has processed and acknowledged the previous one
    chan.basic_qos(prefetch_count=1)

    # receive message and call a func to deal with it
    chan.basic_consume(queue='leo', on_message_callback=callback)

    print(' [Consumer] Waiting for messages. To exit press CTRL+C')

    chan.start_consuming()


def callback(ch, method, properties, body):
    # message handler
    print(' [Consumer] Received %r' % body)
    time.sleep(body.count(b'.'))
    print('[Consumer] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    receive()
