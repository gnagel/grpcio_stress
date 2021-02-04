import grpc
from grpc import aio
from grpc.experimental import aio

import helloworld_pb2
import helloworld_pb2_grpc


async def client_async(server):
    address = f"{server}:50051"
    async with aio.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(1000):
            response = await stub.SayHello(request)
        print(f"Client received: {response}")


def client_sync(server):
    address = f"{server}:50051"
    with grpc.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(1000):
            response = stub.SayHello(request)
        print(f"Client received: {response}")


def test_sync_client_to_sync_server(benchmark):
    def run():
        client_sync("server")

    benchmark(run)


def test_sync_client_to_async_server(benchmark):
    def run():
        client_sync("async_server")

    benchmark(run)


def test_async_client_to_sync_server(benchmark):
    def run():
        client_async("server")

    benchmark(run)


def test_async_client_to_async_server(benchmark):
    def run():
        client_async("server")

    benchmark(run)
