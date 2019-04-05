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

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
chan = conn.channel()

chan.queue_declare('rpc_queue')


def fib(n):
    a, b = 1, 0
    if n == 0:
        return 0
    if n == 1:
        return 1
    for _ in range(1, n):
        a, b = a+b, a
    return a


def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


chan.basic_qos(prefetch_count=1)
chan.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
chan.start_consuming()
