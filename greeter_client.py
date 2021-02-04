import asyncio
import os

import click
import grpc
from grpc import aio
from grpc.experimental import aio

import helloworld_pb2
import helloworld_pb2_grpc


async def client_async():
    address = f"{os.environ['SERVER']}:50051"
    async with aio.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(1000):
            response = await stub.SayHello(request)
        print(f"Client received: {response}")


def client_sync():
    address = f"{os.environ['SERVER']}:50051"
    with grpc.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(1000):
            response = stub.SayHello(request)
        print(f"Client received: {response}")


@click.group()
def cli():
    pass


@cli.command()
def run_async():
    asyncio.run(client_async())


@cli.command()
def run_sync():
    client_sync()


if __name__ == '__main__':
    cli()
