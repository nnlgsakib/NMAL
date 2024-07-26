from nmal import *
from neccak import *
from nlgsecp256k1 import *
from nlg256 import *
from ncrypt import *

# Test the nlg256 with a sample input
test_data = "yooo"
nlg_hash = nlg256(test_data.encode())
print(f"NLGmal nlg-256 hash: {nlg_hash}")

# Test the Neccak-256 implementation with a sample input
test_data = "Hello, NLGmal!"
nlg_hash = neccak256(test_data.encode())
print(f"NLGmal Neccak-256 hash: {nlg_hash}")

# Example usage for conversion functions
decimal_number = 2348734523487374477
nlgmal_number = "mn12pos"

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
message = b"Hello, NLG256!"
signature = sign_message(private_key, message)
print("Signature:", signature)

# Verify the signature
is_valid = verify_signature(public_key, message, signature)
print("Signature valid:", is_valid)


#encryption

# User-defined key (must be a string)
key_str = "1000"
key = key_from_string(key_str)  # Convert to a 256-bit ncryptkey  key

# User-defined data to encrypt
data = b"https://ulam2.0.ulamchain.io/"

# Encrypt the data
encrypted_data, iv = encrypt_data(key, data)
print(f"Encrypted Data (NLGmal): {encrypted_data}")
print(f"IV (NLGmal): {iv}")

# Decrypt the data
decrypted_data = decrypt_data(key, encrypted_data, iv)
print(f"Decrypted Data: {decrypted_data.decode()}")