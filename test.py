from parsec import Parsec
import argparse

parser = argparse.ArgumentParser(description="Test script for using parsec through PyParsec.")
parser.add_argument("socket_path", type=str)
args = parser.parse_args()

# Test sending messages down the socket.
parsec = Parsec(args.socket_path)
parsec.set_provider(1)

parsec.psa_generate_ecc_keypair("anotherKey4")
print(parsec.psa_export_key("anotherKey4").hex())