from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage
from parsec_stream import ParsecStream
from messages.ping_pb2 import Operation, Result
#Serialize to String

class ParsecPing(ParsecMessage):
    def __init__(self):
        super(ParsecMessage)
        self.header.opcode = ParsecMessageOpcode.OP_PING
        
def ping(stream):
    #returns a tuple with the wire protocol versions
    msg = ParsecMessage()
    reply = stream.send(msg)
    majwire = reply.wire_protocol_version_maj
    minwire = reply.wire_protocol_version_min
    return (majwire, minwire)
