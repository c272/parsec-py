from messages.psa_export_key import Operation as PSAExportKeyOperation
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# Represents a message for PSA key export within Parsec.
class PSAExportKeyMessage(ParsecMessage):
	def __init__(self, key_name):
		self.header.opcode = ParsecMessageOpcode.OP_PSA_EXPORT_KEY
		operation = PSAExportKeyOperation()
		operation.key_name = key_name
		self.body = bytes(operation)