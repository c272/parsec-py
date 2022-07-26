
BUILD_DIR=$(shell pwd)

proto : messages/*_pb2.py

messages/%_pb2.py : protobuf/%.proto
	mkdir -p $(dir $@)
	protoc --python_out=$(dir $@) --proto_path=$(word 1,$(dir $^)) $(notdir $^)

.PHONY: clean
clean:
	rm -r messages
