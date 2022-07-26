from operations.ping import ParsecPing
from parsec_header import ParsecHeader
from parsec_message import ParsecMessage
from parsec_stream import ParsecStream

import argparse

parser = argparse.ArgumentParser(description="Test script for using parsec through PyParsec.")
parser.add_argument("socket_path", type=str)
args = parser.parse_args()


# Test sending messages down the socket.
# Open the stream.
stream = ParsecStream()
stream.parsec_socket_path = args.socket_path
stream.connect()

# Craft a message.
message = ParsecMessage()
message.body = "Test!"
message.authentication = bytearray()

# Send a message through the stream.
response = stream.send(message)
print("Response length = " + str(len(response.body)))

# Ping the API.
(majwire, minwire) = ParsecPing()
print("Min Wire Protocol Version")
print(minwire)
print("\n")
print("Max Wire Protocol Version")
print(majwire)
