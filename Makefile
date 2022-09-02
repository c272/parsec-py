PROTO_FILES := $(wildcard protobuf/*.proto)

protobuf:
	mkdir -p messages
	protoc --python_betterproto_out=messages --proto_path=protobuf $(PROTO_FILES)

.PHONY: protobuf clean
clean:
	rm -r messages
