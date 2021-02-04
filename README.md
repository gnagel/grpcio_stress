# Sample app for benchmarking Python 3 + GRPC / GRPC.AIO

## Setup

    docker-compose build

    docker-compose up -d

## Running the tests

To run the tests you can use pytest with the `benchmark` container:

    docker-compose exec benchmark pytest -v test.py --benchmark-min-rounds=10

    ============================================================================================== test session starts ===============================================================================================
    ...
    
    -------------------------------------------------------------------------------------- benchmark: 3 tests --------------------------------------------------------------------------------------
    Name (time in s)                         Min               Max              Mean            StdDev            Median               IQR            Outliers     OPS            Rounds  Iterations
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    test_async_client_to_sync_server      1.0315 (1.0)      1.0575 (1.0)      1.0477 (1.0)      0.0080 (1.29)     1.0484 (1.0)      0.0117 (1.91)          2;0  0.9545 (1.0)          10           1
    test_async_client_to_async_server     2.0282 (1.97)     2.0561 (1.94)     2.0401 (1.95)     0.0084 (1.36)     2.0394 (1.95)     0.0100 (1.63)          4;0  0.4902 (0.51)         10           1
    test_sync_client_to_sync_server       2.0694 (2.01)     2.0925 (1.98)     2.0800 (1.99)     0.0062 (1.0)      2.0792 (1.98)     0.0061 (1.0)           2;1  0.4808 (0.50)         10           1
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
The goal of this test is to benchmark the performance change when migrating to an async environment.

The async client, connecting to a synchronous or asyncconous server should be faster than a synchronous client/server pairing. 