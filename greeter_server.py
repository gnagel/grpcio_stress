import asyncio
from concurrent import futures

import click
import grpc
from grpc import aio

import helloworld_pb2
import helloworld_pb2_grpc


async def serve_async():
    class Greeter(helloworld_pb2_grpc.GreeterServicer):
        async def SayHello(self, request, context):
            return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    server = aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


def serve_sync():
    class Greeter(helloworld_pb2_grpc.GreeterServicer):

        def SayHello(self, request, context):
            return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


@click.group()
def cli():
    pass


@cli.command()
def run_async():
    asyncio.run(serve_async())


@cli.command()
def run_sync():
    serve_sync()


if __name__ == '__main__':
    cli()
