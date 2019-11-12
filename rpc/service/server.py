# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

import logging
import grpc
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


def _serve():
    http_address = '0.0.0.0:5556'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LeoFlaskServicer_to_server(Greeter(), server)
    server.add_insecure_port(http_address)
    print(' * Rpc starting on',  http_address)
    server.start()
    server.wait_for_termination()


def run():
    p = Process(target=_serve)
    p.start()


if __name__ == '__main__':
    logging.basicConfig()
    run()
