#! /usr/bin/env python
import grpc
import logging
from dns import resolver
from dns.exception import DNSException

from test.rpc_test.client.leoflask_test_pb2 import HelloRequest
from test.rpc_test.client.leoflask_test_pb2_grpc import LeoFlaskStub

# 连接consul服务，作为dns服务器
consul_resolver = resolver.Resolver()
consul_resolver.port = 8600
consul_resolver.nameservers = ["127.0.0.1"]


def get_ip_port():
    """查询出可用的一个ip，和端口"""
    try:
        dnsanswer = consul_resolver.query("leorpc.service.consul", "A")
        dnsanswer_srv = consul_resolver.query("leorpc.service.consul", "SRV")
    except DNSException:
        return None, None
    return dnsanswer[0].address, dnsanswer_srv[0].port


_HOST, _PORT = get_ip_port()
print(_HOST, _PORT)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(f'{_HOST}:{_PORT}') as channel:
        stub = LeoFlaskStub(channel)
        response = stub.SayHello(HelloRequest(name='HIHIHI'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(HelloRequest(name="Again"))
        print(response)
        print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
