import socket
import random
from parsec_message import ParsecMessage
from parsec_header import ParsecHeader

class ParsecStream:
    """Represents a simple class to interact with the Parsec Unix domain socket."""

    # The path of the Unix domain socket that Parsec is running on.
    parsec_socket_path = "/run/parsec/parsec.sock"

    # The socket being utilised by this object.
    socket = socket.socket()

    # Randomly generated session identifier.
    session_id = 0

    # Connects to the Parsec socket.
    def connect(self):
        self.session_id = random.randint(0, 0xFFFFFFFF)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.parsec_socket_path)

    # Disconnects from the Parsec socket.
    def disconnect(self):
        self.socket.close()

    # Sends the given Parsec message to the Parsec stream, and awaits a response.
    def send(self, msg: ParsecMessage):
        # Set message session ID header.
        msg.header.session_handle = self.session_id

        # Send serialised message to stream.
        self.socket.sendall(msg.serialise())

        # Await the header response.
        response = ParsecMessage()
        header = ParsecHeader()
        header_buf = bytearray()
        while len(header_buf) < ParsecHeader.HEADER_LENGTH:
            header_buf.extend(self.socket.recv(ParsecHeader.HEADER_LENGTH - len(header_buf)))
        header.deserialise(header_buf)

        # Await the expected extra number of bytes.
        content_buf = bytearray()
        while len(content_buf) < header.content_length and header.content_length != 0:
            content_buf.extend(self.socket.recv(header.content_length - len(content_buf)))

        # Combine, and deserialise.
        response_bytes = bytearray()
        response_bytes.extend(header_buf)
        response_bytes.extend(content_buf)
        response.deserialise(response_bytes)
        return response