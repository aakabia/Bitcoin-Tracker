import requests
import os
# cSpell:ignore dotenv 
from dotenv import load_dotenv
import smtplib
from datetime import datetime

load_dotenv()



def send_Email_To_SMS(body:str)-> None:

    """
    Sends an email-to-SMS message containing the latest cryptocurrency data.

    Parameters:
    body (str): The message content to be sent.

    Returns:
    None
    """

   


    EMAIL_ADDRESS = os.getenv("EMAIL")  # Your email
    EMAIL_PASSWORD = os.getenv("APP_PASSWORD")  # Your email password

    # cSpell:ignore tmomail
    # T-Mobile SMS gateway
    TO_NUMBER = os.getenv("PHONE_NUM") + "@tmomail.net"

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    # create server and port 

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = "Bitcoin Tracker History"
    body = body
    message = f"Subject: {subject}\n\n{body}"

    try:
        # Use STARTTLS for port 587 (recommended for sending emails)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_NUMBER, message)
            print("Message sent successfully")
            return
    except Exception as e:
        print(f"Error: {e}")

def get_Coin_Prices(symbol:str)-> dict:

    """
    Fetches the latest cryptocurrency data for a given symbol.

    Parameters:
    symbol (str): The ticker symbol of the cryptocurrency (e.g., 'BTC' for Bitcoin).

    Returns:
    dict: A dictionary containing the latest price, volume change, percent change, 
          market cap dominance, and last updated timestamp.
    """




    # access the API key from the environment variables & load in requests library
    api_key = os.getenv('API_KEY')

    if not api_key:
        print("API key not found! Check your .env file.")
        exit()

    # check if API Key has loaded properly

    coin_Api_Url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

    params = {
        'symbol': f'{symbol}',  # Bitcoin symbol
        'convert': 'USD'   # Convert to USD
    }

    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accept': 'application/json'
    }

    # set url for api request, params from the request and headers that include your api key 

    response = requests.get(coin_Api_Url, headers=headers, params=params)

    # use the request.get with you url, headers and params as arguments. In future, explore session from request library here!


    if response.status_code == 200:
    
        response_json = response.json()  # Try to parse the JSON response
        coin_Price = round(response_json["data"][symbol][0]["quote"]["USD"]["price"],2)
        coin_Volume_Change_24h = response_json["data"][symbol][0]["quote"]["USD"]["volume_change_24h"]
        coin_Percent_Change_1h = response_json["data"][symbol][0]["quote"]["USD"]["percent_change_1h"]
        coin_Market_Cap_Dominance = response_json["data"][symbol][0]["quote"]["USD"]["market_cap_dominance"]

      
        # receive nested data from dict returned 

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(formatted_time)

        return {
            "coin_Price":coin_Price ,
            "coin_Volume_Change_24h":coin_Volume_Change_24h,
            "coin_Percent_Change_1h": coin_Percent_Change_1h,
            "coin_Market_Cap_Dominance":coin_Market_Cap_Dominance,
            "symbol":symbol,
            "last_Updated_Time_Stamp": formatted_time
            
        }
       
    else:
        print("Unexpected response format: No data found.") 
        print(f"Error {response.status_code}: {response.text}") 

    # error handling and checking if the request is successful

def create_Body(*args:dict)->str:

    """
    Takes multiple cryptocurrency data dictionaries, formats them into structured messages, 
    and combines them into a final message.

    Parameters:
    *args (dict): One or more dictionaries containing cryptocurrency data.

    Returns:
    str: A formatted string containing the latest price, volume change, percent change, 
         market cap dominance, and last updated timestamp for each provided cryptocurrency.
    """





    coin_Descriptions = [
        f"""
        Hello, this is the Most Recent Coin Data!

        {coin["symbol"]} --

        Price: {coin['coin_Price']}

        Volume Change (24h): {coin['coin_Volume_Change_24h']}

        Percent Change (1h): {coin['coin_Percent_Change_1h']}

        Market Cap Dominance: {coin['coin_Market_Cap_Dominance']}

        Time Stamp: {coin['last_Updated_Time_Stamp']}
        """
        for coin in args
    ]

    # Above uses List comprehension to create our list of coin descriptions.

    final_message = "\n\n".join(coin_Descriptions)

    return final_message

def app()->None:

    """
    Creates Bitcoin and Ethereum data, formats it into a message body, 
    and sends it via email to SMS to the user.

    Parameters:
    None

    Returns:
    None
    """


    try:
        BTC_Data = get_Coin_Prices("BTC")
        ETH_Data = get_Coin_Prices("ETH")
        body = create_Body(BTC_Data,ETH_Data) 
        send_Email_To_SMS(body)
        return 
    except Exception as e:
        print(f"Error: {e}")

    # try except block for better error handling when running script


print("hello World")


if __name__ == "__main__":
    app()


# only run script if source is main 
    

