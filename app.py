import requests
import os
from dotenv import load_dotenv
import smtplib
from datetime import datetime

load_dotenv()



def send_Email_To_SMS(body):

    EMAIL_ADDRESS = os.getenv("EMAIL")  # Your email
    EMAIL_PASSWORD = os.getenv("APP_PASSWORD")  # Your email password

    # T-Mobile SMS gateway
    TO_NUMBER = os.getenv("PHONE_NUM") + "@tmomail.net"

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    # creater server and port 

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

def get_Coin_Prices():


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
        btc_Price = round(response_json["data"]["BTC"][0]["quote"]["USD"]["price"],2)
        btc_Volume_Change_24h = response_json["data"]["BTC"][0]["quote"]["USD"]["volume_change_24h"]
        btc_Percent_Change_1h = response_json["data"]["BTC"][0]["quote"]["USD"]["percent_change_1h"]
        btc_Market_Cap_Dominance = response_json["data"]["BTC"][0]["quote"]["USD"]["market_cap_dominance"]

        # receive nested data from dict returned 

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(formatted_time)

        return {
            "btc_Price":btc_Price ,
            "btc_Volume_Change_24h":btc_Volume_Change_24h,
            "btc_Percent_Change_1h": btc_Percent_Change_1h,
            "btc_Market_Cap_Dominance":btc_Market_Cap_Dominance,
            "last_Updated_Time_Stamp": formatted_time
            
        }
       
    else:
        print("Unexpected response format: No data found.") 
        print(f"Error {response.status_code}: {response.text}") 

    # error handeling and checking if the request is successful

def create_Body(coin_dict):


    bodyMessage =f"""
        Hello this is the Most Recent Bitcoin Data!

        BITCOIN!

        price: {coin_dict['btc_Price']}

        Volume_Change_24h: {coin_dict['btc_Volume_Change_24h']}

        Percent_Change_1h: {coin_dict['btc_Percent_Change_1h']}

        Market_Cap_Dominance: {coin_dict['btc_Market_Cap_Dominance']}

        Time_Stamp: {coin_dict['last_Updated_Time_Stamp']}

           
        """
    
    # create the body useing our dict from get_Coin_Prices
    
    return bodyMessage

def app():

    try:
        data = get_Coin_Prices()
        body = create_Body(data) 
        send_Email_To_SMS(body)
        return 
    except Exception as e:
        print(f"Error: {e}")

    # try except block to for better error handeling when running script



if __name__ == "__main__":
    app()


# only run script if source is main 
    

