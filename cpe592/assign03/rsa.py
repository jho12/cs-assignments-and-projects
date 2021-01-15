# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

# Due to the implementation of the secrets module, please use Python 3.6
# or higher. This program was implemented with Python 3.8.0.

# Additionally, because this program deals with 2048-bit integers, this
# program will take a couple minutes to complete.

from math import gcd   # imports GCD function in math module
import secrets         # secrets module; requires Python 3.6+

msg = 'JustinHo'                # String to be encrypted
msg_len = len(msg)              # Length of string
enc = msg.encode()              # Encodes string to bytes object
p = int.from_bytes(enc, 'big')  # Conversion of encoding to integer
bitlength = 2048                # Bit length of prime numbers
bitlength_max = 4096            # Maximum bit length
num_rounds = 20                 # Number of rounds done with Miller-Rabin test

# Miller-Rabin primality test for finding a sufficiently large prime
# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
def miller_rabin_test (test_cand, rounds=num_rounds):
    if test_cand == 2:       # 2 is the only even prime
        return True
    if not (test_cand & 1):  # test_cand not odd; thus cannot be prime
        return False

    r = 0
    d = test_cand - 1

    while (d % 2 == 0):  # while d is divisible by 2
        d >>= 1          # divide d by 2
        r += 1           # increment r

    # ensure test_cand is of the form 2^r * d + 1 and d is odd
    assert test_cand == 2**r * d + 1 and (d & 1)

    # Helper function for testing primality;
    # allows for continues in witness loop
    def test (x,r,t):
        for i in range(r-1):
            x = square_and_multiply(x, 2, t)
            if x == t - 1:
                return True
        return False

    # Witness test loop; repeat rounds times
    for i in range(rounds):
        # Pick random odd a in range [2, test_cand-2]
        # i.e., choose random a in group Zp
        a = 2 + secrets.randbelow(test_cand - 3)

        x = square_and_multiply(a, d, test_cand)  # x = (a^d) mod test_cand

        # If true, x passes this round of testing
        if x == 1 or x == test_cand-1:
            continue

        # If true, x passes this round of testing
        if test(x, rounds, test_cand):
            continue

        return False  # If loop reaches this, test_cand is composite

    # If test_cand passes all rounds, it is probably prime
    # The chance of test_cand being composite is on the order of
    # 10^-111 when num_rounds = 20 and bitlength = 2048
    return True

# Generates prime tuple (p,q)
def generate_primes (n=bitlength):
    assert n >= bitlength and n <= bitlength_max

    print('Generating prime candidates...\n')

    p_candidate = secrets.randbits(n)
    q_candidate = secrets.randbits(n)

    print('Testing prime candidate p...')
    while True:
        if miller_rabin_test(p_candidate, num_rounds):
            break
        p_candidate = p_candidate + 1
    print('Prime candidate found: p =', p_candidate)

    print('\nTesting prime candidate q...')
    while True:
        if miller_rabin_test(q_candidate, num_rounds):
            break
        q_candidate = q_candidate + 1
    print('Prime candidate found: q =', q_candidate)

    return (p_candidate, q_candidate)

# Below two methods are an implementation of the Extended Euclidean Algorithm, from
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def xgcd(a, b):
    # return (g, x, y) such that a*x + b*y = g = gcd(a, b)
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def modinv(a, b):
    # return x such that (x * a) % b == 1
    g, x, _ = xgcd(a, b)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return x % b

# Generates the public and private keys
def generate_keys ():
    p, q = generate_primes()

    n = p * q

    # Lambda(n): Carmichael's totient function;
    # Lambda(n) = lcm(p-1, q-1)
    #           = |(p-1) * (q-1)| / gcd(p-1, q-1)
    # Used according to https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    lm = (p-1) * (q-1) // gcd(p-1, q-1)

    print('\nGenerating keys...')

    while True:  # Loop until a suitable e is found
        e = 2 + secrets.randbelow(lm - 2)  # choose e s.t. 1 < e < lambda(n)

        if gcd(e, lm) == 1:    # Suitable e found
            d = modinv(e, lm)  # Now find d
            assert (d * e) % lm == 1  # ensure d = e^-1 mod lm
            break  # d and e are found; exit loop

    key_pub = (e,n)  # generated public key
    key_pvt = (d,n)  # generated private key

    print('Keys generated!')
    print('Public key tuple:', key_pub)
    print('\nPrivate key tuple:', key_pvt)

    return (key_pub, key_pvt)

# Square-and-multiply algorithm, relatively efficient algorithm from
# https://incolumitas.com/2018/08/12/finding-large-prime-numbers-and-rsa-miller-rabin-test/
def square_and_multiply (x, k, n=None):
    b = bin(k).lstrip('0b')
    r = 1
    for i in b:
        r = r**2
        if i == '1':
            r *= x
        if n:
            r %= n
    return r

# RSA encryption
def encrypt (p, key_pub):
    e, n = key_pub
    return square_and_multiply(p, e, n)

# RSA decryption
def decrypt (c, key_pvt):
    d, n = key_pvt
    return square_and_multiply(c, d, n)

if __name__ == '__main__':
    key_pub, key_pvt = generate_keys()

    print('\nMessage to be encrypted:', msg)
    print('Encoded plaintext:', p)

    c = encrypt(p, key_pub)

    print('Ciphertext:', c)

    d = decrypt(c, key_pvt)
    m = (d.to_bytes(msg_len, 'big')).decode()

    print('Decrypted ciphertext:', d)
    print('Decoded ciphertext:', m)
