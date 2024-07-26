from nmal import *
from neccak import *
from nlgsecp256k1 import *
from nlg256 import *
from ncrypt import *

# Test the nlg256 with a sample input
test_data = "NLG"
nlg_hash = nlg256(test_data.encode())
print(f"NLGmal nlg-256 hash: {nlg_hash}")

# Test the Neccak-256 implementation with a sample input
test_data = "NLG"
nlg_hash = neccak256(test_data.encode())
print(f"NLGmal Neccak-256 hash: {nlg_hash}")

# Example usage for conversion functions
decimal_number = 10000
nlgmal_number = "t8s"

# Convert decimal to NLGmal
converted_to_nlgmal = decimal_to_nlgmal(decimal_number)
print(f"Decimal {decimal_number} to NLGmal: {converted_to_nlgmal}")

# Convert NLGmal to decimal
converted_to_decimal = nlgmal_to_decimal(nlgmal_number)
print(f"NLGmal {nlgmal_number} to Decimal: {converted_to_decimal}")

# Generate a private key
private_key = generate_private_key()
print("Private Key:", decimal_to_nlgmal(private_key))

# Generate the corresponding public key
public_key = generate_public_key(private_key)
print("Public Key:", public_key)

# Sign a message
message = b"NLG"
signature = sign_message(private_key, message)
print("Signature:", signature)

# Verify the signature
is_valid = verify_signature(public_key, message, signature)
print("Signature valid:", is_valid)


# #encryption
#
# Example usage
key_str = "1000"

# User-defined data to encrypt
data = b"NLG"
print(f"Input Data: {data}")

# Encrypt the data
encrypted_data_str = encrypt_data(key_str, data)
print(f"Encrypted Data (Plain List): {encrypted_data_str}")

# Decrypt the data
decrypted_data = decrypt_data(key_str, encrypted_data_str)
print(f"Decrypted Data: {decrypted_data.decode()}")