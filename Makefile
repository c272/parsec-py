
BUILD_DIR=$(shell pwd)

proto : messages/psa/*_pb2.py

messages/psa/%_pb2.py : protobuf/psa_%.proto
	echo $^
	protoc --python_out=${BUILD_DIR}/psa --proto_path=$(word 1,$(dir $^)) $(notdir $^)
