import requests
import json


# This function gets keys (ICO currency code) through values (currency names).
# It takes a currency name and turns it into the corresponding ICO code.
def currency_name_to_ico(currency_name):
    return list(currency_list.keys())[list(currency_list.values()).index(currency_name)]


# This currency takes 2 ICO currency codes
# and gives the exchange rate of the first currency to the second currency.
def exchange_rate_get(from_ico, to_ico):
    return(json.loads(requests.get
           (f"https://api.frankfurter.dev/v1/latest?base={from_ico}&symbols={to_ico}").text)["rates"][to_ico])


# Main Routine

# This line of code first requests a list of all currencies from the API using the requests.get method.
# Then, the output from the API is given to the json.loads method, in text format.
# This converts it into a dictionary. currency_list is a dictionary.
# This dictionary is important and is used for currency_name_to_ico, along with the rest of the main routine.
currency_list = json.loads(requests.get("https://api.frankfurter.dev/v1/currencies").text)

# Prints the dictionary on its own,
# then prints the keys (ICO currency code) and values (names) of each currency separately.
print(currency_list)
print()
print("Keys")
print(list(currency_list.keys()))
print()
print("Values")
print(list(currency_list.values()))
print()

while True:
    try:
        input_currency_ico = currency_name_to_ico(input("name of input currency? "))
        break
    except ValueError:
        print("this currency does not exist. try again")
        pass

while True:
    try:
        output_currency_ico = currency_name_to_ico(input("name of output currency? "))
        break
    except ValueError:
        print("this currency does not exist. try again")
        pass

print(f"The exchange rate from {input_currency_ico} to {output_currency_ico}"
      f" is {exchange_rate_get(input_currency_ico, output_currency_ico)}.")

# This code is extremely pedantic and requires the spelling and capitalisation of names to be exact,
# but this is OK because this component will be used with a combo box (dropdown) which has no way of making a typo.
