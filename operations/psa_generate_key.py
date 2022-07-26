from parsec_message import ParsecMessage
import key_attributes
import protobuf


class GenerateKey(ParsecMessage):

    def __init__(self, key_name: str, attributes: key_attributes.KeyAttributes):

        self.header.opcode = 0x0002
        self.key_name = key_name
        self.attributes = attributes




