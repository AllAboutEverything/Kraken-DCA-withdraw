# This Python script implements a simple way to dollar-cost averaging on Kraken.com

# Instructions:
# 1. Add your API keys to the script below
# 2. Define the trading pair you wish to use (e.g., exchanging Monero XMR with Euro EUR)
# 3. Ensure Python and the 'requests' library are installed on your computer
# 4. Schedule the script to run regularly (e.g., using the Windows Task Scheduler) for daily execution

import urllib.parse
import hashlib
import hmac
import base64
import time
import os
import requests

# add your personal Kraken API key and secret
api_url = "https://api.kraken.com"
api_key = "insert your api key here" # add your api key
api_sec = "insert your api secret here" # add your api secret

# Authenticated requests should be signed with the "API-Sign" header, using a signature generated with your private key, nonce, encoded payload
def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

# We need the current price of the crypto coin you wanna buy, because on kraken we can only request an order denominated in crypto, not fiat
def get_xmr_price():
    resp = requests.get(f'https://api.kraken.com/0/public/Ticker?pair=XXMRZEUR').json() # specify trading pair
    ask_price = resp['result']['XXMRZEUR']['a'][0] # specify trading pair
    return float(ask_price)
   
# Calculate the cryptocurrency quantity to purchase using your fiat amount and the current coin price
def calculate_volume_from_price() -> float:
    volume = 20 / get_xmr_price() # Modify the value in this line to specify the desired investment amount
    return volume

# Construct the request and print the result
resp = kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "market",
    "type": "buy",
    "pair": "XMREUR",  # specify trading pair
    "volume": calculate_volume_from_price(),
    
}, api_key, api_sec)

print(resp.json())
