from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

from messages.psa_generate_key_pb2 import Operation,Result
from messages.psa_key_attributes_pb2 import KeyAttributes, KeyType, UsageFlags, KeyPolicy
from messages.psa_algorithm_pb2 import Algorithm

class Message(ParsecMessage):
    def __init__(self, body):
        super().__init__()
        self.header.opcode = ParsecMessageOpcode.OP_PSA_SIGN_HASH
        self.body = body.SerializeToString()

def psa_generate_ecc_key_pair(stream, key_name, bits, family=KeyType.EccFamily.SECP_R1, hash_type=Algorithm.SHA_256):
    op = Operation()
    op.key_name = key_name
    op.attributes.key_type.ecc_key_pair.curve_family = family
    op.attributes.key_bits = bits
    op.attributes.key_policy.key_usage_flags.sign_hash = True
    op.attributes.key_policy.key_usage_flags.verify_hash = True
    op.attributes.key_policy.key_algorithm.hash = hash_type  

    msg = Message(op)

    reply = Result()
    reply.ParseFromString(stream.send(msg).body.encode("utf-8"))

    return Result.ParseFromString(reply).signature

__all__ = ["psa_generate_ecc_key_pair"]
