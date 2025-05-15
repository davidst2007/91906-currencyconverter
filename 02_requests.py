import requests
import json

# This line of code first requests a list of all currencies from the API using the requests.get method.
# Then, the output from the API is given to the json.loads method, in text format.
# This converts it into a dictionary. currency_list is a dictionary.
currency_list = json.loads(requests.get("https://api.frankfurter.dev/v1/currencies").text)

# Prints the dictionary on its own,
# then prints the keys (ICO currency code) and values (names) of each currency seperately.
print(currency_list)
print()
print("Keys")
print(list(currency_list.keys()))
print()
print("Values")
print(list(currency_list.values()))
print()

# This code gets keys (ICO currency code) through values (currency names).
# It uses Australian Dollar as an example.
aud_ico = list(currency_list.keys())[list(currency_list.values()).index("Australian Dollar")]

# Gets the exchange rate from NZD to AUD, by using the code from earlier that finds keys from values.
nzd_to_aud = (json.loads(requests.get
              (f"https://api.frankfurter.dev/v1/latest?base=NZD&symbols={aud_ico}").text)["rates"][aud_ico])

# Prints the exchange rate from NZD to AUD.
print(nzd_to_aud)
print(f"1 NZD is worth {nzd_to_aud} in {aud_ico}.")
