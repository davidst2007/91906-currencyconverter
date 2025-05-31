import requests
import json

# This is intended to be imported into main file.

# This function gets keys (ICO currency code) through values (currency names).
# It takes a currency name and turns it into the corresponding ICO code.
def currency_name_to_ico(currency_name):
    return list(currency_list.keys())[list(currency_list.values()).index(currency_name)]


# This currency takes 2 ICO currency codes
# and gives the exchange rate of the first currency to the second currency.
def exchange_rate_get(from_ico, to_ico):
    print(f"https://api.frankfurter.dev/v1/latest?base={from_ico}&symbols={to_ico}")
    print(json.loads(requests.get(f"https://api.frankfurter.dev/v1/latest?base={from_ico}&symbols={to_ico}").text))
    return(json.loads(requests.get
           (f"https://api.frankfurter.dev/v1/latest?base={from_ico}&symbols={to_ico}").text)["rates"][to_ico])


# This line of code first requests a list of all currencies from the API using the requests.get method.
# Then, the output from the API is given to the json.loads method, in text format.
# This converts it into a dictionary. currency_list is a dictionary.
# This dictionary is important and is used for currency_name_to_ico, along with the rest of the main routine.
currency_list = json.loads(requests.get("https://api.frankfurter.dev/v1/currencies").text)
