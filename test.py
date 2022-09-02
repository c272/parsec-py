from messages.psa_algorithm import AlgorithmHash
from messages.psa_key_attributes import KeyType, KeyTypeEccFamily, KeyTypeEccKeyPair, KeyTypeRawData
from parsec import Parsec
import argparse

parser = argparse.ArgumentParser(description="Test script for using parsec through PyParsec.")
parser.add_argument("socket_path", type=str)
args = parser.parse_args()

# Test sending messages down the socket.
parsec = Parsec(args.socket_path)
parsec.set_provider(1)

# # Ping the API.
# (majwire, minwire) = parsec.ping()
# parsec.ping()
# parsec.ping()
# print("Min Wire Protocol Version")
# print(minwire)
# print("Max Wire Protocol Version")
# print(majwire)

parsec.psa_generate_ecc_keypair("anotherKey4")
print(parsec.psa_export_key("anotherKey4").hex())