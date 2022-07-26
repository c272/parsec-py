from messages.psa_export_public_key_pb2 import Operation,Result
from parsec_message import ParsecMessage

class Message(ParsecMessage):
	def __init__(self, body):
		super().__init__()
		self.header.opcode = 0x0007
		self.body = body.SerializeToString()

def psa_export_public_key(stream, key_name):
	op = Operation()
	op.key_name = key_name

	msg = Message(op)
	
	reply = stream.send(msg)
	return reply.data

__all__ = ["psa_export_public_key"]
