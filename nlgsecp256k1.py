import random
from nmal import *

# SECP256k1 curve parameters in NLGmal
P = decimal_to_nlgmal(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
A = decimal_to_nlgmal(0)
B = decimal_to_nlgmal(7)
Gx = decimal_to_nlgmal(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
Gy = decimal_to_nlgmal(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
N = decimal_to_nlgmal(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)

def mod_inverse(a, p):
    """Compute the modular inverse of a modulo p."""
    lm, hm = 1, 0
    low, high = a % p, p
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % p

def elliptic_curve_add(P, Q, p):
    """Elliptic curve point addition."""
    if P == Q:
        return elliptic_curve_double(P, p)
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P

    x1, y1 = nlgmal_to_decimal(P[0]), nlgmal_to_decimal(P[1])
    x2, y2 = nlgmal_to_decimal(Q[0]), nlgmal_to_decimal(Q[1])

    m = (y2 - y1) * mod_inverse(x2 - x1, p) % p
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return decimal_to_nlgmal(x3), decimal_to_nlgmal(y3)

def elliptic_curve_double(P, p):
    """Elliptic curve point doubling."""
    if P == (None, None):
        return P

    x1, y1 = nlgmal_to_decimal(P[0]), nlgmal_to_decimal(P[1])
    a = nlgmal_to_decimal(A)

    m = (3 * x1**2 + a) * mod_inverse(2 * y1, p) % p
    x3 = (m**2 - 2 * x1) % p
    y3 = (m * (x1 - x3) - y1) % p

    return decimal_to_nlgmal(x3), decimal_to_nlgmal(y3)

def elliptic_curve_multiply(k, P, p):
    """Elliptic curve scalar multiplication."""
    N = P
    Q = (None, None)
    while k:
        if k & 1:
            Q = elliptic_curve_add(Q, N, p)
        N = elliptic_curve_double(N, p)
        k >>= 1
    return Q

def generate_private_key():
    """Generate a random private key."""
    return random.getrandbits(256) % nlgmal_to_decimal(N)

def generate_public_key(private_key):
    """Generate the corresponding public key for a given private key."""
    p = nlgmal_to_decimal(P)
    G = (Gx, Gy)
    return elliptic_curve_multiply(private_key, G, p)

def sign_message(private_key, message):
    """Sign a message using the private key."""
    z = int.from_bytes(message, 'big')
    k = random.getrandbits(256) % nlgmal_to_decimal(N)
    p = nlgmal_to_decimal(P)
    G = (Gx, Gy)
    R = elliptic_curve_multiply(k, G, p)
    r = nlgmal_to_decimal(R[0]) % nlgmal_to_decimal(N)
    s = (mod_inverse(k, nlgmal_to_decimal(N)) * (z + r * private_key)) % nlgmal_to_decimal(N)
    return decimal_to_nlgmal(r), decimal_to_nlgmal(s)

def verify_signature(public_key, message, signature):
    """Verify a message signature."""
    r, s = nlgmal_to_decimal(signature[0]), nlgmal_to_decimal(signature[1])
    z = int.from_bytes(message, 'big')
    w = mod_inverse(s, nlgmal_to_decimal(N))
    p = nlgmal_to_decimal(P)
    G = (Gx, Gy)
    u1 = (z * w) % nlgmal_to_decimal(N)
    u2 = (r * w) % nlgmal_to_decimal(N)
    P1 = elliptic_curve_multiply(u1, G, p)
    P2 = elliptic_curve_multiply(u2, public_key, p)
    R = elliptic_curve_add(P1, P2, p)
    return nlgmal_to_decimal(R[0]) % nlgmal_to_decimal(N) == r
