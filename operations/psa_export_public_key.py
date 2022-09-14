from messages.psa_export_public_key import Operation as PSAExportPublicKeyOperation
from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# Represents a message for PSA public key export within Parsec.
class PSAExportPublicKeyMessage(ParsecMessage):
    def __init__(self, key_name):
        self.header.opcode = ParsecMessageOpcode.OP_PSA_EXPORT_PUBLIC_KEY
        op = PSAExportPublicKeyOperation()
        op.key_name = key_name
        self.body = bytes(op)