from encodings import utf_8
from enum import IntEnum
from parsec_header import ParsecHeader


class ParsecMessage:
    """Class to represent a single Parsec message, either a request or a response."""

    # The header of the Parsec request.
    header = ParsecHeader()

    # The body of the request. A string, as outputted by a Protobuf Python class.
    body = ""

    # The authentication footer of the request.
    authentication = bytearray()

    # Writes the current request to file.
    # You do not need to manually set header lengths, this function will perform that for you.
    def serialise(self):
        body_bytes = bytearray(self.body, "utf8")

        # Set header lengths.
        self.header.auth_length = len(self.authentication)
        self.header.content_length = len(body_bytes)

        # Serialise header, append body & authentication.
        final_bytes = bytearray(self.header.serialise())
        final_bytes.extend(body_bytes)
        final_bytes.extend(self.authentication)

        return final_bytes

    # Deserialises the given request bytes into this request object.
    def deserialise(self, bytes):
        self.header.deserialise(bytes[0:ParsecHeader.HEADER_LENGTH])
        auth_start_idx = ParsecHeader.HEADER_LENGTH + self.header.content_length
        self.body = bytes[ParsecHeader.HEADER_LENGTH:auth_start_idx].decode("utf-8")

        # If there is an authentication part, get that too.
        if self.header.auth_length > 0:
            self.authentication = bytearray(bytes[auth_start_idx:])

    # Returns whether this Parsec message represents an error response.
    def is_error(self):
        return self.header.status != 0

class ParsecMessageErrorType(IntEnum):
    """Represents the type of error returned by the Parsec message."""
    WRONG_PROVIDER_ID = 1
    CONTENT_TYPE_UNSUPPORTED = 2
    ACCEPT_TYPE_UNSUPPORTED = 3
    WIRE_PROTOCOL_VER_UNSUPPORTED = 4
    PROVIDER_NOT_REGISTERED = 5
    INVALID_PROVIDER = 6
    BODY_DESERIALISE_FAILED = 7
    BODY_SERIALISE_FAILED = 8
    INVALID_OPCODE = 9
    RESPONSE_TOO_LARGE = 10
    AUTH_ERROR = 11
    AUTH_NOT_EXIST = 12
    AUTH_NOT_REGISTERED = 13
    KEY_INFO_MANAGER_ERROR = 14
    CONNECTION_ERROR = 15
    INVALID_ENCODING = 16
    INVALID_HEADER = 17
    WRONG_PROVIDER_UUID = 18
    NOT_AUTHENTICATED = 19
    BODY_SIZE_EXCEEDS_LIMIT = 20
    ADMIN_REQUIRED = 21
    PSA_GENERIC_ERROR = 1132
    PSA_NOT_PERMITTED = 1133
    PSA_NOT_SUPPORTED = 1134
    PSA_INVALID_ARG = 1135
    PSA_INVALID_HANDLE = 1136
    PSA_BAD_STATE = 1137
    PSA_BUF_TOO_SMALL = 1138
    PSA_ALREADY_EXISTS = 1139
    PSA_DOES_NOT_EXIST = 1140
    PSA_INSUFFICIENT_MEMORY = 1141
    PSA_INSUFFICIENT_STORAGE = 1142
    PSA_INSUFFICIENT_DATA = 1143
    PSA_COMMS_FAILURE = 1145
    PSA_STORAGE_FAILURE = 1146
    PSA_HARDWARE_FAILURE = 1147
    PSA_INSUFFICIENT_ENTROPY = 1148
    PSA_INVALID_SIG = 1149
    PSA_INVALID_PADDING = 1150
    PSA_TAMPERED = 1151
    PSA_CORRUPTED = 1152