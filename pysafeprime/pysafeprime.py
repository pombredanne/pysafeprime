import sys
import os
import math
import struct

def _random_in_range(low, high):
    num_bytes = (int(math.log(high, 2)) / 8) + 1
    n = int(os.urandom(num_bytes).encode('hex'), 16)
    while n < low or n > high:
        n = int(os.urandom(num_bytes).encode('hex'), 16)
    return n

def _random_bit_integer(bits):
    low = (2 ** bits) + 1
    high = (2 ** (bits + 1)) - 1
    return _random_in_range(low, high)

def is_prime(n, t = 1):
    '''
    Miller-Rabin primality test algorithm 4.24 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''

    if n % 2 == 0:
        return False

    nn = n - 1
    s = 0
    while nn % 2 == 0:
        s += 1
        nn /= 2
    r = nn

    assert((2 ** s) * r == (n - 1))

    for i in range(1):
        a = _random_in_range(2, n - 2)
        y = pow(a, r, n)
        if y != 1 and y != (n - 1):
            j = 1
            while j <= s - 1 and y != (n - 1):
                y = pow(y, y, n)
                if y == 1:
                    return False
                j = j + 1
            if y != (n - 1):
                return False
    return True

def random_prime(k, t = 1):
    '''
    Random prime generation algorithm 4.44 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''
    num_trials = 10000
    trial = 0
    while trial < num_trials:
        n = _random_bit_integer(k)
        if is_prime(n, t):
            return n
        trial += 1

def safe_prime(k, tt = 1):
    '''
    Safe prime generation algorithm 4.53 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''

    s = random_prime(k, tt)
    t = random_prime(k, tt)

    i = 1
    q = 0
    while q == 0:
        qt = (2 * i * t) + 1
        if is_prime(qt, tt):
            q = qt
        i += 1

    r = q

    p0 = (2 * (pow(s, r - 2, r)) * s) - 1

    j = 1
    q = 0
    while q == 0:
        qt = p0 + (2 * j * r * s)
        if is_prime(qt, tt):
            q = qt
        j += 1

    p = q

    return p

def fast_safe_prime(k, tt = 1):
    # https://eprint.iacr.org/2003/175.pdf
    pass

# TODO: translate t parameter into probability
# test passes with probability at most (1/4^t) on a composite number

# print is_prime(15, 10)
# print is_prime(23, 10)
# print random_prime(100, 100)
# print safe_prime(100, 100)
