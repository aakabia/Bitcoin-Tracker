import requests
import os
from dotenv import load_dotenv
load_dotenv()


# access the API key from the environment variables & load in requests library
api_key = os.getenv('API_KEY')

if not api_key:
    print("API key not found! Check your .env file.")
    exit()

# check if API Key has loaded properly

bitcoin_api_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

params = {
    'symbol': 'BTC',  # Bitcoin symbol
    'convert': 'USD'   # Convert to USD
}

headers = {
    'X-CMC_PRO_API_KEY': api_key,
    'Accept': 'application/json'
}

# set url for api request, params from the request and headers that include your api key 

response = requests.get(bitcoin_api_url, headers=headers, params=params)

# use the request.get with you url, headers and params as arguments. In future, explore session from request library here!


if response.status_code == 200:
    
    response_json = response.json()  # Try to parse the JSON response
    print(type(response_json)) 
else:
    print("Unexpected response format: No data found.") 
    print(f"Error {response.status_code}: {response.text}") 

# error handeling and checking if the request is successful
    

