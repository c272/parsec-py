import operations.ping
from parsec_header import ParsecHeader
from parsec_message import ParsecMessage
from parsec_stream import ParsecStream

import operations.psa_generate_key

import argparse

parser = argparse.ArgumentParser(description="Test script for using parsec through PyParsec.")
parser.add_argument("socket_path", type=str)
args = parser.parse_args()


# Test sending messages down the socket.
# Open the stream.
stream = ParsecStream()
stream.parsec_socket_path = args.socket_path
stream.connect()

# Ping the API.
(majwire, minwire) = operations.ping.ping(stream)
print("Min Wire Protocol Version")
print(minwire)
print("\n")
print("Max Wire Protocol Version")
print(majwire)

#result = operations.psa_generate_key.psa_generate_ecc_key_pair(stream, "generated key", 256)
#print(result)
