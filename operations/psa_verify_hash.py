from messages.psa_export_public_key import Operation,Result
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# todo: cleanup to new API

class VerifyHash(ParsecMessage):
    def __init__(self, body):
        super(ParsecMessage)
        self.header.opcode = ParsecMessageOpcode.OP_PSA_VERIFY_HASH
        self.body = body.SerializeToString()

def psa_verify_hash(stream, key_name, alg, hash, signature):
    op = Operation()
    op.key_name = key_name
    op.alg = alg
    op.hash = hash
    op.signature = signature

    msg = VerifyHash(op)
    reply = Result()
    reply.ParseFromString(stream.send(msg).body.encode("utf-8"))
    return True
    

__all__ = ["psa_verify_hash"]
