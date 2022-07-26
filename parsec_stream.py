from enum import IntEnum
import os
import socket
import random
from parsec_message import ParsecMessage
from parsec_header import ParsecHeader
from parsec_enums import *

class ParsecMessageException(Exception):
    """Represents a single message exception returned from the Parsec stream."""
    status_code = 0

    def __init__(self, msg: ParsecMessage):
        status_code = ParsecMessageErrorType(msg.header.status)


class ParsecStream:
    """Represents a simple class to interact with the Parsec Unix domain socket."""

    # The path of the Unix domain socket that Parsec is running on.
    parsec_socket_path = "/run/parsec/parsec.sock"

    # The socket being utilised by this object.
    socket = socket.socket()

    # Randomly generated session identifier.
    session_id = 0

    # The authentication type this stream is using.
    auth_type = ParsecAuthenticationType.NO_AUTH
    auth_app_id = ""
    auth_proc_uid = 0

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

        # Set the authentication footer based on type.
        msg.header.auth_type = int(self.auth_type)
        if self.auth_type == ParsecAuthenticationType.DIRECT_AUTH:
            msg.authentication = self.auth_app_id.encode()
        elif self.auth_type == ParsecAuthenticationType.UNIX_PEER_AUTH:
            msg.authentication = self.auth_proc_uid
        elif self.auth_type == ParsecAuthenticationType.NO_AUTH:
            msg.authentication = bytearray() # Do nothing.
        else:
            print("WARN: Unsupported authentication type used. Ignoring auth footer...")

        # Set content & authentication length.
        msg.header.content_length = len(msg.body.encode())
        msg.header.auth_length = len(msg.authentication)

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

        # If the response contains an error, throw an exception.
        if response.is_error():
            raise ParsecMessageException(response)
            
        return response

    # Enables direct authentication mode, using the supplied application identity string (UTF8).
    def enable_direct_authentication(self, application_identity: str):
        self.auth_type = ParsecAuthenticationType.DIRECT_AUTH
        self.auth_app_id = application_identity

    def enable_unix_peer_authentication(self):
        self.auth_type = ParsecAuthenticationType.UNIX_PEER_AUTH
        self.auth_proc_uid = os.getuid()