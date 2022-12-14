import struct

from parsec_enums import ParsecAuthenticationType, ParsecMessageErrorType, ParsecMessageOpcode

class ParsecHeader:
    """A simple class to represent the fixed Parsec header."""

    # Static length of the header in bytes.
    HEADER_LENGTH = 36

    # Identifies the back-end service provider for which the request is intended. 
    provider = 0

    # Session handle.
    session_handle = 0

    # Authentication type (requests only).
    auth_type = ParsecAuthenticationType.NO_AUTH

    # Length of the attached content (bytes).
    content_length = 0

    # Length of the authentication section (bytes, request only).
    auth_length = 0

    # Opcode.
    opcode = ParsecMessageOpcode.NOOP

    # Status (responses only).
    status = ParsecMessageErrorType.SUCCESS

    # Serialises the current state of the Parsec header into valid bytes.
    def serialise(self):
        # Define magic values (unchanging).
        magic_bytes = 0x5EC0A710
        header_remainder = 30
        major_version = 0x1
        minor_version = 0x0
        flags = 0x0000
        content_type = 0x0
        accept_type = 0x0
        resv = 0

        # Pack into struct.
        return struct.pack("=IHBBHBQBBBIHIHH", 
            magic_bytes,
            header_remainder,
            major_version,
            minor_version,
            flags,
            self.provider,
            self.session_handle,
            content_type,
            accept_type,
            int(self.auth_type),
            self.content_length,
            self.auth_length,
            int(self.opcode),
            int(self.status),
            resv)

    # Deserializes the given byte buffer into this header structure.
    def deserialise(self, buf):
        # Unpack from struct.
        header_tuple = struct.unpack("=IHBBHBQBBBIHIHH", buf)

        self.provider = header_tuple[5]
        self.session_handle = header_tuple[6]
        self.auth_type = ParsecAuthenticationType(header_tuple[9])
        self.content_length = header_tuple[10]
        self.auth_length = header_tuple[11]
        self.opcode = ParsecMessageOpcode(header_tuple[12])
        self.status = ParsecMessageErrorType(header_tuple[13])