from ..parsec_enums import ParsecMessageOpcode
from ..parsec_message import ParsecMessage

from messages import psa_generate_key_pb2
from messages import psa_key_attributes_pb2

import key_attributes

import protobuf


class GenerateKey(ParsecMessage):

    def __init__(self, key_name: str, attributes: key_attributes.KeyAttributes):

        self.header.opcode = ParsecMessageOpcode.OP_PSA_GENERATE_KEY
        self.key_name = key_name
        self.attributes = attributes

        proto_attributes = psa_key_attributes_pb2.KeyAttributes()
