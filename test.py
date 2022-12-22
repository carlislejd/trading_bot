import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

token = getenv('TELEGRAM')
userID = 'carlisle trade bot'
message = 'Here is my first message'

# Create url
url = f'https://api.telegram.org/bot{token}/sendMessage'

# Create json link with message
data = {'chat_id': userID, 'text': message}

# POST the message
requests.post(url, data)