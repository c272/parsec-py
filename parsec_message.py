from parsec_header import ParsecHeader

class ParsecMessage:
    """Class to represent a single Parsec message, either a request or a response."""

    # The header of the Parsec message.
    header = ParsecHeader()

    # The bytes body of the message.
    body = bytes()

    # The authentication footer of the message.
    authentication = bytearray()

    # Writes the current request to file.
    # You do not need to manually set header lengths, this function will perform that for you.
    def serialise(self):
        # Set header lengths.
        self.header.auth_length = len(self.authentication)
        self.header.content_length = len(self.body)

        # Serialise header, append body & authentication.
        final_bytes = bytearray(self.header.serialise())
        final_bytes.extend(self.body)
        final_bytes.extend(self.authentication)

        return final_bytes

    # Deserialises the given request bytes into this request object.
    def deserialise(self, bytes):
        self.header.deserialise(bytes[0:ParsecHeader.HEADER_LENGTH])
        auth_start_idx = ParsecHeader.HEADER_LENGTH + self.header.content_length
        self.body = bytes[ParsecHeader.HEADER_LENGTH:auth_start_idx]

        # If there is an authentication part, get that too.
        if self.header.auth_length > 0:
            self.authentication = bytearray(bytes[auth_start_idx:])

    # Returns whether this Parsec message represents an error response.
    def is_error(self):
        return self.header.status != 0