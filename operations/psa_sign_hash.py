from messages.psa_sign_hash_pb2 import Operation,Result
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

class SignHashMessage(ParsecMessage):
	def __init__(self, body):
		super().__init__()
		self.header.opcode = ParsecMessageOpcode.OP_PSA_SIGN_HASH
		self.body = body.SerializeToString()

def psa_sign_hash(stream, key_name, hash_msg, algorithm):
	op = Operation()
	op.key_name = key_name
	op.alg = algorithm
	op.hash = hash_msg

	msg = SignHashMessage(op)
	
	reply = stream.send(msg)
	return reply.signature

__all__ = ["psa_sign_hash"]
