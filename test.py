from ast import parse
import parsec_header

header = parsec_header.ParsecHeader()
header.content_length = 3920
header.auth_type = 3
header.opcode = 0x2
header.session_handle = 0xEEEEEEEE

byte_head = header.serialise()
rev_head = parsec_header.ParsecHeader()
rev_head.deserialise(byte_head)
print("session handle: " + str(rev_head.session_handle))