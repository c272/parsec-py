from operations.psa_export_public_key import PSAExportPublicKeyMessage
from parsec_message import ParsecMessage
from parsec_stream import ParsecStream
from operations.ping import PingMessage
from operations.psa_export_key import PSAExportKeyMessage
from operations.psa_generate_key import PSAGenerateECCKeypairMessage
from messages.ping import Result as PingResult
from messages.psa_export_key import Result as PSAExportKeyResult
from messages.psa_export_public_key import Result as PSAExportPublicKeyResult
from messages.psa_algorithm import AlgorithmHash
from messages.psa_key_attributes import KeyTypeEccFamily, UsageFlags

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

    # Sends a Parsec message to the currently targeted provider.
    def send_to_provider(self, msg: ParsecMessage, proto_out = None):
        msg.header.provider = self.target_provider
        return self.stream.send(msg, proto_out)

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
        msg = PSAExportKeyMessage(key_name)
        reply = PSAExportKeyResult()
        self.send_to_provider(msg, reply)

        return reply.data

    def psa_export_public_key(self, key_name):
        msg = PSAExportPublicKeyMessage(key_name)
        reply = PSAExportPublicKeyResult()
        self.send_to_provider(msg, reply)

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
        msg = PSAGenerateECCKeypairMessage(key_name, family, bits, hash_type, usage_flags)
        self.send_to_provider(msg)