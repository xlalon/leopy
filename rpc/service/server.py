#! /usr/bin/env python
# -*- coding: utf8 -*-

import grpc
import time
import consul
from concurrent import futures
from multiprocessing import Process

from rpc.service.leoflask_pb2 import HelloReply
from rpc.service.leoflask_pb2_grpc import  LeoFlaskServicer, add_LeoFlaskServicer_to_server


class Greeter(LeoFlaskServicer):

    def SayHello(self, request, context):
        return HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        print(request)
        return HelloReply(message='HelloAgain, %s!' % request.name)


def register(service_name, host, port):
    print("register started...")
    # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
    c = consul.Consul()
    # 健康检查的ip，端口，检查时间
    check = consul.Check.tcp(host, port, "30s")
    # 注册服务
    c.agent.service.register(
        f"{service_name}",
        f"{service_name}-{host}",
        address=host,
        port=port,
        check=check
    )
    print("leorpc注册服务成功")
    print("services: " + str(c.agent.services()))


def unregister(port):
    print("unregister started")
    c = consul.Consul()
    c.agent.service.deregister(f"leorpc-{port}")


def _serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LeoFlaskServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + str(port))
    register('leorpc', host, port)
    server.start()
    print(f"{port} server start success")
    try:
        while True:
            time.sleep(180000)
    except KeyboardInterrupt:
        unregister(port)
        server.stop(0)


def run(host='127.0.0.1', port=5556):
    Process(target=_serve, args=(host, port)).start()


if __name__ == '__main__':
    pass
    # logging.basicConfig()
    # run()
