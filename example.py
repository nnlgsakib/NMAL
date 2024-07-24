from nccak  import *
from nlg256 import *
from nlgsecp256k1 import *

def genkeypair():
    priv_key, pub_key = generate_keypair()
    print(f"Private Key (NLG256): {private_key_to_nlg256(priv_key)}")
    print(f"Public Key (NLG256): {public_key_to_nlg256(pub_key)}")
    print(f"Address: {address_from_public_key(pub_key)}")

genkeypair()

# Test the nlg256 with a sample input
test_data = "yooo"
nlg_hash = nlg256(test_data.encode())
print(f"NLGmal nlg-256 hash: {nlg_hash}")

# Test the implementation with a sample input
test_data = "Hello, NLGmal!"
nlg_hash = neccak256(test_data.encode())
print(f"NLGmal Neccak-256 hash: {nlg_hash}")

# Example usage
decimal_number = int(input("Add some decimal number to convert into NLGDECIMAL: "))
nlgmal_number = input("Add some NLGDECIMAL to convert it into Decimal : ")

# Convert decimal to NLGmal
converted_to_nlgmal = decimal_to_nlgmal(decimal_number)
print(f"Decimal {decimal_number} to NLGmal: {converted_to_nlgmal}")

# Convert NLGmal to decimal
converted_to_decimal = nlgmal_to_decimal(nlgmal_number)
print(f"NLGmal {nlgmal_number} to Decimal: {converted_to_decimal}")
