# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from .leoflask_pb2 import *


class LeoFlaskStub(object):
  """service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SayHello = channel.unary_unary(
        '/leoflask.LeoFlask/SayHello',
        request_serializer=HelloRequest.SerializeToString,
        response_deserializer=HelloReply.FromString,
        )
    self.SayHelloAgain = channel.unary_unary(
        '/leoflask.LeoFlask/SayHelloAgain',
        request_serializer=HelloRequest.SerializeToString,
        response_deserializer=HelloReply.FromString,
        )


class LeoFlaskServicer(object):
  """service definition.
  """

  def SayHello(self, request, context):
    """Sends a greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SayHelloAgain(self, request, context):
    """Sends another greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_LeoFlaskServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SayHello': grpc.unary_unary_rpc_method_handler(
          servicer.SayHello,
          request_deserializer=HelloRequest.FromString,
          response_serializer=HelloReply.SerializeToString,
      ),
      'SayHelloAgain': grpc.unary_unary_rpc_method_handler(
          servicer.SayHelloAgain,
          request_deserializer=HelloRequest.FromString,
          response_serializer=HelloReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'leoflask.LeoFlask', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
