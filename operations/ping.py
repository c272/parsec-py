from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage

# Represents a message to request the version of the current Parsec wire protocol.
class PingMessage(ParsecMessage):
    def __init__(self):
        self.header.opcode = ParsecMessageOpcode.OP_PING