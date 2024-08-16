# nmal.py
# license: MIT
# This script implements a custom number system named "NLG DECIMAL" (shortened to "NLGmal").
# The NLGmal number system uses the characters 0-9 and m-z, making it a base-24 system.
# This script includes functions to convert decimal numbers to NLGmal and vice versa.

# Defining the NLGmal characters
NLGmal_chars = "0123456789mnopqrstuvwxyz"

base = len(NLGmal_chars)

# Dictionary for quick look-up of character values
char_to_value = {char: idx for idx, char in enumerate(NLGmal_chars)}


def decimal_to_nlgmal(decimal):
    """Convert a decimal number to an NLGmal number."""
    if decimal == 0:
        return NLGmal_chars[0]

    nlgmal = ""
    while decimal > 0:
        nlgmal = NLGmal_chars[decimal % base] + nlgmal
        decimal //= base
    return nlgmal


def nlgmal_to_decimal(nlgmal):
    """Convert an NLGmal number to a decimal number."""
    # Check for capital letters and issue a warning
    if any(char.isupper() for char in nlgmal):
        print("Warning: Capital letters detected. Its good to use small  letter. Please be carefull next time :)")
        nlgmal = nlgmal.lower()

    decimal = 0
    for char in nlgmal:
        decimal = decimal * base + char_to_value[char]
    return decimal


def bytes_to_nlgdecimal(byte_data):
    """Convert bytes to an NLGmal string."""
    # Convert bytes to a decimal number
    decimal_number = int.from_bytes(byte_data, byteorder='big')
    # Convert decimal number to NLGmal
    return decimal_to_nlgmal(decimal_number)

def nlgdecimal_to_bytes(nlgdecimal):
    """Convert an NLGmal string to bytes."""
    # Convert NLGmal to decimal number
    decimal_number = nlgmal_to_decimal(nlgdecimal)
    # Convert decimal number to bytes
    # Determine the number of bytes required
    num_bytes = (decimal_number.bit_length() + 7) // 8
    return decimal_number.to_bytes(num_bytes, byteorder='big')
