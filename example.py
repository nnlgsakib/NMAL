from NLGMAL import *


# Example usage
decimal_number = int(input("Add some decimal number to convert into NLGDECIMAL: "))
nlgmal_number = input("Add some NLGDECIMAL to convert it into Decimal : ")

# Convert decimal to NLGmal
converted_to_nlgmal = decimal_to_nlgmal(decimal_number)
print(f"Decimal {decimal_number} to NLGmal: {converted_to_nlgmal}")

# Convert NLGmal to decimal
converted_to_decimal = nlgmal_to_decimal(nlgmal_number)
print(f"NLGmal {nlgmal_number} to Decimal: {converted_to_decimal}")
