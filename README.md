# parsec-py
A Parsec client library for the Python 3 world. Implements interaction with the wire protocol along with a minimal subset of the Parsec operations.

## Building
Building `parsec-py` has two dependencies for protobuf:
- `protoc`
- `betterproto`
You can install `protoc` through your choice of package manager (on apt this is `protobuf-compiler`), and betterproto through `pip install "betterproto[compiler]"`. To build the protobuf files, simply run `make protobuf`.

## Usage
To connect to the Parsec daemon, you will have to know what socket is being listened on. By default, this is `/run/parsec/parsec.sock`, however if you're using the quick start download version of Parsec this will be different.
```
stream = ParsecStream()
stream.parsec_socket_path = args.socket_path
stream.connect()
```

After this point, you can send commands through Parsec.
```
# Ping the API.
(majwire, minwire) = operations.ping.ping(stream)
```