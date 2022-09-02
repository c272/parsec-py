from parsec_enums import ParsecMessageOpcode
from parsec_message import ParsecMessage
from messages.psa_generate_key import Operation as PSAGenerateKeyOperation

# Represents a message requesting to generate a key or keypair on a given provider.
class PSAGenerateECCKeypairMessage(ParsecMessage):
    def __init__(self, provider, key_name, family, bits, hash_type, usage_flags):
        self.header.opcode = ParsecMessageOpcode.OP_PSA_GENERATE_KEY
        self.header.provider = provider
        operation = PSAGenerateKeyOperation()
        operation.key_name = key_name
        operation.attributes.key_type.ecc_key_pair.curve_family = family
        operation.attributes.key_bits = bits
        operation.attributes.key_policy.key_usage_flags = usage_flags
        operation.attributes.key_policy.key_algorithm.hash = hash_type

        self.body = bytes(operation)