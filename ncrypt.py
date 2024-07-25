from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from nmal import *
import hashlib
import os


def bytes_to_decimal(data):
    """Convert bytes to a list of decimal numbers."""
    return [int.from_bytes(data[i:i + 16], 'big') for i in range(0, len(data), 16)]


def decimal_to_bytes(decimals):
    """Convert a list of decimal numbers to bytes."""
    byte_list = []
    for decimal in decimals:
        byte_list.append(decimal.to_bytes(16, 'big'))
    return b''.join(byte_list)


def encrypt_data(key, data):
    """Encrypt data using AES and convert to NLGmal."""
    # Generate a random IV
    iv = os.urandom(16)

    # Pad data
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # AES Encryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Convert encrypted data to decimal
    encrypted_decimals = bytes_to_decimal(encrypted_data)

    # Convert decimal to NLGmal
    return [decimal_to_nlgmal(dec) for dec in encrypted_decimals], decimal_to_nlgmal(int.from_bytes(iv, 'big'))


def decrypt_data(key, encrypted_data, iv):
    """Decrypt NLGmal encrypted data and return the original data."""
    # Convert NLGmal to decimal
    encrypted_decimals = [nlgmal_to_decimal(dec) for dec in encrypted_data]
    iv = nlgmal_to_decimal(iv).to_bytes(16, 'big')

    # Convert decimal to bytes
    encrypted_bytes = decimal_to_bytes(encrypted_decimals)

    # AES Decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Unpad data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data


def key_from_string(key_str):
    """Convert a string key to a 256-bit AES key."""
    # Hash the string key to ensure it is 256 bits
    return hashlib.sha256(key_str.encode()).digest()