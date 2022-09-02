from parsec_stream import ParsecStream
from operations.ping import PingMessage
from operations.psa_export_key import PSAExportKeyMessage
from operations.psa_generate_key import PSAGenerateECCKeypairMessage
from messages.ping import Result as PingResult
from messages.psa_export_key import Result as PSAExportKeyResult
from messages.psa_generate_key import Result as PSAGenerateKeyResult
from messages.psa_algorithm import AlgorithmAeadAeadWithDefaultLengthTag, AlgorithmAsymmetricSignatureEcdsa, AlgorithmAsymmetricSignatureEcdsaAny, AlgorithmHash, AlgorithmMac, AlgorithmMacFullLength, AlgorithmMacFullLengthCmac, AlgorithmNone
from messages.psa_key_attributes import KeyTypeAes, KeyTypeEccFamily, KeyTypeEccKeyPair, KeyTypeRawData, UsageFlags

class Parsec:
    """Represents an instance of the Parsec API, with a stream to the Parsec socket."""

    # The provider that this API is currently targeting.
    # By default, set to the universal provider.
    # This provider is only attached to messages that do not have to be targeted at the universal provider.
    target_provider = 0

    # Initialises the Parsec API stream, using a custom socket path if provided.
    def __init__(self, socketPath = ""):
        self.stream = ParsecStream()
        if socketPath:
            self.stream.socket_path = socketPath

    # Sets the current target provider for this API.
    def set_provider(self, provider: int):
        self.target_provider = provider

    # Pings the Parsec daemon for the current wire protocol version.
    def ping(self):
        msg = PingMessage()
        reply = PingResult()
        self.stream.send(msg, reply)

        return (reply.wire_protocol_version_maj, reply.wire_protocol_version_min)

    # Exports an existing PSA key in binary format.
    # Returns an array of bytes containing the key data.
    def psa_export_key(self, key_name):
        msg = PSAExportKeyMessage(self.target_provider, key_name)
        reply = PSAExportKeyResult()
        self.stream.send(msg, reply)

        return reply.data

    # Generates a new ECC keypair given the key name, type, and other parameters.
    # Throws ParsecMessageException on fail, returns void on success.
    def psa_generate_ecc_keypair(self, key_name, family=KeyTypeEccFamily.SECP_K1, bits=256, hash_type=AlgorithmHash.SHA_256, usage_flags=None):
        # Set up default usage flags if none passed.
        if usage_flags == None:
            usage_flags = UsageFlags()
            usage_flags.export = True
            usage_flags.sign_hash = True
            usage_flags.sign_message = True
            usage_flags.verify_hash = True
            usage_flags.verify_message = True

        # Send message.
        msg = PSAGenerateECCKeypairMessage(self.target_provider, key_name, family, bits, hash_type, usage_flags)
        self.stream.send(msg)