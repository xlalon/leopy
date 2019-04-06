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
import uuid


class FibRpcClient:

    def __init__(self):

        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.chan = self.conn.channel()

        result = self.chan.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.chan.basic_consume(queue=self.callback_queue,
                                on_message_callback=self.on_response,
                                auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.corr_id = str(uuid.uuid4())
        self.chan.basic_publish(exchange='',
                                routing_key='rpc_queue',
                                properties=pika.BasicProperties(
                                    reply_to=self.callback_queue,
                                    correlation_id=self.corr_id),
                                body=str(n))
        while self.response is None:
            self.conn.process_data_events()

        return int(self.response)


fib = FibRpcClient()
print(" [x] Requesting fib(30)")
response = fib.call(30)
print(" [.] Got %r" % response)








