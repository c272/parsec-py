from messages.psa_sign_hash import Operation as PSASignHashOperation
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# Represents a single Parsec message to sign a precalculated hash with a private key.
class PSASignHashMessage(ParsecMessage):
    def __init__(self, key_name, hash_msg, alg):
        self.header.opcode = ParsecMessageOpcode.OP_PSA_SIGN_HASH
        op = PSASignHashOperation()
        op.key_name = key_name
        op.hash = hash_msg
        op.alg = alg
        self.body = bytes(op)