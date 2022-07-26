from parsec_header import ParsecHeader
from parsec_message import ParsecMessage

# Header testing.
header = ParsecHeader()
header.content_length = 3920
header.auth_type = 3
header.opcode = 0x2
header.session_handle = 0xEEEEEEEE

byte_head = header.serialise()
rev_head = ParsecHeader()
rev_head.deserialise(byte_head)
print("session handle: " + str(rev_head.session_handle) + "\n")

# Message testing.
request = ParsecMessage()
request.header = header
request.body = "This is a test!"
request.authentication = bytearray([0xE, 0xE, 0xE, 0xE, 0xE])
req_encoded = request.serialise()

req_decoded = ParsecMessage()
req_decoded.deserialise(req_encoded)
print("body = " + req_decoded.body)
print("auth = " + str(req_decoded.authentication))