from messages.psa_export_key_pb2 import Operation,Result
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

class Message(ParsecMessage):
	def __init__(self, body):
		super().__init__()
		self.header.opcode = ParsecMessageOpcode.OP_PSA_EXPORT_KEY
		self.body = body.SerializeToString()

def psa_export_key(stream, key_name):
	op = Operation()
	op.key_name = key_name

	msg = Message(op)
	
	reply = stream.send(msg)
	return reply.data

__all__ = ["psa_export_key"]
