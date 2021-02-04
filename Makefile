.PHONY: protos

_default: protos

protos:
	python -m grpc.tools.protoc -I./ --python_out=. --grpc_python_out=. ./helloworld.proto
