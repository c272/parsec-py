from messages.psa_verify_hash import Operation as PSAVerifyHashOperation
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# Represents a Parsec message to verify the signature of a hash or short message using a public key.
class PSAVerifyHashMessage(ParsecMessage):
    def __init__(self, key_name, alg, hash, signature):
        self.header.opcode = ParsecMessageOpcode.OP_PSA_VERIFY_HASH
        op = PSAVerifyHashOperation()
        op.key_name = key_name
        op.alg = alg
        op.hash = hash
        op.signature = signature
        self.body = bytes(op)