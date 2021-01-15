# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

from array import array
import os

# Input filenames (original, LSB, MSB, respectively)
org_input_filename = 'bird.bmp'
lsb_input_filename = 'lsb.bmp'
msb_input_filename = 'msb.bmp'

# Filesizes of input files
org_filesize = os.path.getsize(org_input_filename)
lsb_filesize = os.path.getsize(lsb_input_filename)
msb_filesize = os.path.getsize(msb_input_filename)

# Stegano key
key = (1600*3) * 500 + (1200*3)

# Pseudo-macros
size_byte = 8
msg_length = 8
msg_bit_length = size_byte * msg_length

# Byte arrays for input files
org_bin = array('B')
lsb_encoding = array('B')
msb_encoding = array('B')

# Byte arrays for decoding of stenographs
lsb_decode = array('B')
msb_decode = array('B')

# Loading byte arrays with file info
with open(org_input_filename, 'rb') as org_file:
    org_bin.fromfile(org_file, org_filesize)
org_file.close()

with open(lsb_input_filename, 'rb') as lsb_file:
    lsb_encoding.fromfile(lsb_file, lsb_filesize)
lsb_file.close()

with open(msb_input_filename, 'rb') as msb_file:
    msb_encoding.fromfile(msb_file, msb_filesize)
msb_file.close()

# Decodes the stenographs, recording XOR bits indicating hidden message
counter = 0
while counter < msg_bit_length:
    lsb_decode.append(lsb_encoding[key + counter] ^ org_bin[key + counter])
    msb_decode.append((msb_encoding[key + counter] ^ org_bin[key + counter]) >> 7)
    counter += 1

# Helper function that converts the decoded bit array into a byte array
def bits_to_bytes(bits, msg_length):
    byte = array('B')
    for i in xrange(msg_length):
        byte.append(0)
        for j in xrange(size_byte):
            byte[i] |= (bits[i*size_byte + j] << (size_byte - j - 1))
    return byte

# Prints decoded message
print 'LSB decoding: ' + bits_to_bytes(lsb_decode, msg_length).tostring()
print 'MSB decoding: ' + bits_to_bytes(msb_decode, msg_length).tostring()
