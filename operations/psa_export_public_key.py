from messages.psa_export_public_key_pb2 import Operation,Result
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

class Message(ParsecMessage):
    def __init__(self, body):
        super().__init__()
        self.header.opcode = ParsecMessageOpcode.OP_PSA_EXPORT_PUBLIC_KEY
        self.body = body.SerializeToString()

def psa_export_public_key(stream, key_name):
    op = Operation()
    op.key_name = key_name

    msg = Message(op)
	
    reply = Result()
    reply.ParseFromString(stream.send(msg).body.encode("utf-8"))
    return reply.data

__all__ = ["psa_export_public_key"]
