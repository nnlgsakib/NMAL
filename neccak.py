import struct
from nmal import *

# SHA-3 (Keccak-256) rotation offsets
RHO_OFFSETS = [
    0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14
]

# SHA-3 (Keccak-256) round constants
THETA_CONSTANTS = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

# Convert SHA-3 (Keccak-256) constants to NLGdecimal number system
RHO_OFFSETS_NLG = RHO_OFFSETS
THETA_NLG = [decimal_to_nlgmal(k) for k in THETA_CONSTANTS]
PI_NLG = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]  # Linear Pi permutation values

def rotr(n, x, bits=64):
    """Rotate right."""
    return ((x >> n) | (x << (bits - n))) & ((1 << bits) - 1)

def neccak_f(state):
    # Neccak-f permutation
    for round_idx in range(24):
        # Theta step
        C = [0] * 5
        D = [0] * 5
        for x in range(5):
            C[x] = state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20]
        for x in range(5):
            D[x] = C[(x - 1) % 5] ^ rotr(1, C[(x + 1) % 5], 64)
        for x in range(25):
            state[x] ^= D[x % 5]

        # Rho and Pi steps
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                rho_offset = RHO_OFFSETS_NLG[(x + 3 * y) % 24]
                B[((PI_NLG[x] * 5) + y) % 25] = rotr(rho_offset, state[x * 5 + y])

        # Chi step
        for x in range(5):
            for y in range(5):
                state[x * 5 + y] = B[x * 5 + y] ^ ((~B[(x + 1) % 5 * 5 + y]) & B[(x + 2) % 5 * 5 + y])

        # Iota step
        state[0] ^= nlgmal_to_decimal(THETA_NLG[round_idx])

def neccak256(data):
    # Initialize state
    state = [0] * 25
    data = bytearray(data)
    data_len = len(data) * 8

    # Padding
    data.append(0x01)
    while len(data) % 200 != 192:
        data.append(0x00)
    data += struct.pack('<Q', data_len)

    # Absorb phase
    for i in range(0, len(data), 200):
        block = data[i:i + 200]
        for j in range(25):
            state[j] ^= struct.unpack('<Q', block[j * 8:(j + 1) * 8])[0]
        neccak_f(state)

    # Squeeze phase
    output = bytearray()
    for _ in range(2):  # Two 64-byte blocks for Neccak-256
        for j in range(25):
            output += struct.pack('<Q', state[j])
        neccak_f(state)

    return ''.join(decimal_to_nlgmal(x) for x in struct.unpack('<32B', output[:32]))  # Return first 256 bits as NLGdecimal
