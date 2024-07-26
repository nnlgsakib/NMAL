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


def key_from_string(key_str):
    """Convert a string key to a 256-bit AES key."""
    return hashlib.sha256(key_str.encode()).digest()


def encrypt_data(key_str, data):
    """Encrypt data using AES and convert to NLGmal list."""
    # Convert key string to a 256-bit AES key
    key = key_from_string(key_str)

    # Generate a random IV
    iv = os.urandom(16)

    # Pad data
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # AES Encryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Combine IV and encrypted data
    combined_data = iv + encrypted_data

    # Convert combined data to decimal
    combined_decimals = bytes_to_decimal(combined_data)

    # Convert decimal to NLGmal and format to plain list
    encrypted_data_list = [decimal_to_nlgmal(dec) for dec in combined_decimals]
    return ','.join(encrypted_data_list)


def decrypt_data(key_str, encrypted_data_str):
    """Decrypt NLGmal encrypted data and return the original data."""
    # Convert key string to a 256-bit AES key
    key = key_from_string(key_str)

    # Convert the plain list format string to a list of NLGmal strings
    encrypted_data_list = encrypted_data_str.split(',')

    # Convert NLGmal to decimal
    combined_decimals = [nlgmal_to_decimal(dec) for dec in encrypted_data_list]

    # Convert decimal to bytes
    combined_bytes = decimal_to_bytes(combined_decimals)

    # Separate IV and encrypted data
    iv = combined_bytes[:16]
    encrypted_bytes = combined_bytes[16:]

    # AES Decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Unpad data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data