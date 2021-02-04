import asyncio
import concurrent

import grpc
from grpc import aio
from grpc.experimental import aio

import helloworld_pb2
import helloworld_pb2_grpc

REQUEST_COUNT = 10
THREAD_COUNT = 10


async def client_async(server):
    address = f"{server}:50051"
    async with aio.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(REQUEST_COUNT):
            response = await stub.SayHello(request)
        return response


def client_sync(server):
    address = f"{server}:50051"
    with grpc.insecure_channel(address) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name='you')
        for i in range(REQUEST_COUNT):
            stub.SayHello(request)


def test_sync_client_to_sync_server(benchmark):
    def run():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for key in range(0, THREAD_COUNT):
                executor.submit(client_sync, "server")

    benchmark(run)


# def test_sync_client_to_async_server(benchmark):
#     def run():
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             for key in range(0, THREAD_COUNT):
#                 executor.submit(client_sync, "async_server")
#         client_sync("async_server")
#
#     benchmark(run)


def test_async_client_to_sync_server(benchmark):
    def run():
        async def main():
            await asyncio.gather(*(client_async("server") for _ in range(0, THREAD_COUNT)))

        asyncio.run(main())

    benchmark(run)


def test_async_client_to_async_server(benchmark):
    def run():
        async def main():
            await asyncio.gather(*(client_async("async_server") for _ in range(0, THREAD_COUNT)))

        asyncio.run(main())

    benchmark(run)
