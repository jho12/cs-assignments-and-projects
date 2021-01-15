# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

from array import array
import os

# Filenames (input, least significant bit, most significant bit, respectively)
input_filename = 'bird.bmp'
lsb_filename = 'lsb.bmp'
msb_filename = 'msb.bmp'

# Filesize of input file for use with Python arrays
filesize = os.path.getsize(input_filename)

# Stegano message
name = 'JustinHo'

# Stegano key
key = (1600*3) * 500 + (1200*3)

# Byte arrays for name and image
bin_name = array('B')
lsb_encode = array('B')
msb_encode = array('B')

# Loads arrays with binary info
bin_name.fromstring(name)

with open(input_filename, 'rb') as lsb_file:
    lsb_encode.fromfile(lsb_file, filesize)
lsb_file.close()

with open(input_filename, 'rb') as msb_file:
    msb_encode.fromfile(msb_file, filesize)
msb_file.close()

# Helper function that turns a byte to an array of bits
# For use with LSB method
def byte_to_bits(byte):
    bits = array('B')
    for i in xrange(8):
        bits.insert(0, (byte >> i) & 1)
    return bits

#Helper function that turns a byte to an array of bits, but the bits are padded to the left
# For use with MSB method
def byte_to_padded_bits(byte):
    bits = array('B')
    for i in xrange(8):
        bits.insert(0, ((byte >> i) & 1) << 7)
    return bits

# Encodes the steno message with LSB method
counter = key
for b_name in bin_name:
    for bit in byte_to_bits(b_name):
        lsb_encode[counter] ^= bit
        counter += 1

# Encodes the steno message with MSB method
counter = key
for b_name in bin_name:
    for bit in byte_to_padded_bits(b_name):
        msb_encode[counter] ^= bit
        counter += 1

lsb_file = open(lsb_filename, 'w+b')
lsb_encode.tofile(lsb_file)
lsb_file.close()

msb_file = open(msb_filename, 'w+b')
msb_encode.tofile(msb_file)
msb_file.close()
