# import requests
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

# cSpell:ignore dotenv
from dotenv import load_dotenv
from datetime import datetime
import requests

# using string placeholder to load from templates directory
env = Environment(loader=FileSystemLoader("%s/templates/" % os.path.dirname(__file__)))

load_dotenv()


def send_Email(body: str) -> None:
    """
    Send an email using user-configured email settings.

    This function sends an email message using the application's
    configured email credentials and settings (e.g., SMTP server,
    sender address, authentication). The provided body is used as
    the email content.

    Args:
        body (str): The email message content to be sent.

    Returns:
        None

    Raises:
        SMTPException: If sending the email fails due to an SMTP error.
        ValueError: If required user configuration is missing or invalid.
    """

    # get email and secure password for sending from your email
    Email = os.getenv("EMAIL")
    Password = os.getenv("PASSWORD")

    # set to and from email
    TO_EMAIL_ADDRESS = os.getenv("TO_EMAIL")
    FROM_EMAIL_ADDRESS = os.getenv("FROM_EMAIL")

    # set subject and message properties
    subject = "Bitcoin Tracker History"
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = FROM_EMAIL_ADDRESS
    message["To"] = TO_EMAIL_ADDRESS

    # attach the MIMEText body as html to the message
    # create the message body as a string
    message.attach(MIMEText(body, "html"))
    msgBody = message.as_string()

    # create server and port
    SMTP_SERVER = "smtp.mail.yahoo.com"
    SMTP_PORT = 587

    # send the email
    try:

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

            server.starttls()  # Secure the connection
            server.login(Email, Password)
            server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, msgBody)
            server.close()  # close connection
            return

    except Exception as e:
        print(f"Error: {e}")


def handle_Send_Email(emailBody: str):
    """
    Handle the email sending process and provide user feedback.

    This function acts as a wrapper around `send_Email`, sending the
    provided message content and printing a confirmation message
    upon successful execution.

    Args:
        emailBody (str): The email body content to be sent.

    Returns:
        None

    Raises:
        Any exception raised by `send_Email` if the email fails to send.
        A TypeError exception if emailBody is not of type "str"
    """

    if type(emailBody) != str:
        raise TypeError("Email body is not of type str! ")

    send_Email(emailBody)
    print("Mail sent successfully.")
    return


def create_email_body(template: str, templateData: dict) -> str:
    """
    Render an email body from a Jinja template using the provided data.

    This function loads a template by name from the configured Jinja
    environment and renders it with the supplied template data.

    Args:
        template (str): The name of the template file to load.
        templateData (dict): A dictionary of values to inject into the template.

    Returns:
        str: The rendered email body as a string.

    Raises:
        TemplateNotFound: If the specified template does not exist.
        TemplateError: If an error occurs during template rendering.
    """

    if type(templateData) != dict:
        raise TypeError("Template data must be of type dict")

    
    template = env.get_template(template)
    
    output = template.render(data=templateData)
    
    return output



# Todo : create function that writes a confirmation message to a file.
# Todo : create a way for user to access this on the go or with a cron job 


def get_Coin_Data(symbol: str) -> dict:
    """
        Fetch real-time cryptocurrency market data from the CoinMarketCap API.

        This function retrieves the latest market information for a specified
        cryptocurrency symbol using the CoinMarketCap Pro API. The API key is
        loaded securely from environment variables.



    Parameters
    ----------
    symbol : str
        The cryptocurrency ticker symbol (e.g., "BTC", "ETH").
        Must be provided as a string.

    Returns
    -------
    dict
        A dictionary containing:
            - coin_Price (float): Current price in USD (rounded to 2 decimals).
            - coin_Volume_Change_24h (float): 24-hour volume change.
            - coin_Percent_Change_1h (float): Percentage price change in the last hour.
            - coin_Market_Cap_Dominance (float): Market cap dominance percentage.
            - symbol (str): Uppercase cryptocurrency symbol.
            - last_Updated_Time_Stamp (str): Timestamp of data retrieval (YYYY-MM-DD HH:MM:SS).

    Raises
    ------
    TypeError
        If the provided symbol is not a string.
    KeyError
        If the cryptocurrency symbol is invalid or not found in the API response.
    Exception
        For general request or response handling errors.

    Notes
    -----
    - Requires a valid CoinMarketCap Pro API key stored in environment variables as 'API_KEY'.
    - Makes a GET request to:
      https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest
    - Converts all prices to USD.
    - Ensure the 'requests', 'os', 'sys', and 'datetime' libraries are imported before calling.

    """

    # access the API key from the environment variables & load in requests library
    api_key = os.getenv("API_KEY")


    # check if API Key has loaded properly
    if not api_key:
        print("API key not found! Check your .env file.")
        sys.exit()
    

    
    if type(symbol) != str:
        raise TypeError("Please use a valid Crypto symbol as a string!")

    try:

        symbol_Upper = symbol.upper()


        # set url for api request, params from the request and headers that include your api key
        
        coin_Api_Url = (
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        )

        params = {
            "symbol": f"{symbol_Upper}",  # Bitcoin symbol
            "convert": "USD",  # Convert to USD
        }

        headers = {"X-CMC_PRO_API_KEY": api_key, "Accept": "application/json"}

        # use the request.get with you url, headers and params as arguments. In future, explore session from request library here!
        response = requests.get(coin_Api_Url, headers=headers, params=params)


        

        if response.status_code == 200:
            # receive nested data from dict returned from response_json
            response_json = response.json()  
            coin_Price = round(
                response_json["data"][symbol_Upper][0]["quote"]["USD"]["price"], 2
            )
            coin_Volume_Change_24h = response_json["data"][symbol_Upper][0]["quote"][
                "USD"
            ]["volume_change_24h"]
            coin_Percent_Change_1h = response_json["data"][symbol_Upper][0]["quote"][
                "USD"
            ]["percent_change_1h"]
            coin_Market_Cap_Dominance = response_json["data"][symbol_Upper][0]["quote"][
                "USD"
            ]["market_cap_dominance"]

         

            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            return {
                "coin_Price": coin_Price,
                "coin_Volume_Change_24h": coin_Volume_Change_24h,
                "coin_Percent_Change_1h": coin_Percent_Change_1h,
                "coin_Market_Cap_Dominance": coin_Market_Cap_Dominance,
                "symbol": symbol_Upper,
                "last_Updated_Time_Stamp": formatted_time,
            }

        else:
            print("Unexpected response format: No data found.")
            print(f"Error {response.status_code}: {response.text}")

    # error handling and checking if the request is successful
    except KeyError as e:
        print(
            f"Error: Please use a valid symbol, '{e}', is not a valid crypto symbol. "
        )
    except TypeError as e:
        print(
            f"Error: value or values you are trying to access for current symbol is not of correct type.  '{e}'"
        )
    except Exception as e:
        print(f"Error: {e}")


def app() -> None:
    """
    Creates crypto data based on user request, formats it into a message body,
    and sends it via email to email to the user.

    Parameters:
    None

    Returns:
    None
    """

    try:
        user_Input = input("Please enter symbol for what crypto coin information would you like?")
        coin_data = get_Coin_Data(user_Input)

        emailBody = create_email_body("Email.html", coin_data)
        handle_Send_Email(emailBody)

        return
    except Exception as e:
        print(f"Error: {e}")

    # try except block for better error handling when running script


# only run script if source is main

if __name__ == "__main__":
    app()
  
