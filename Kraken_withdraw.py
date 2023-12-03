# This Python script implements a simple way to withdraw crypto from Kraken.com to your cold storage

# Instructions:
# 1. Add your API keys to the script below
# 2. Specify the cryptocurrency you intend to withdraw (e.g., Monero XMR)
# 3. Additionally, below, add the name assigned to your cold storage wallet on Kraken
# 4. Ensure Python and the 'requests' library are installed on your computer
# 5. Schedule the script to run regularly (e.g., using the Windows Task Scheduler) for monthly execution

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

# Construct the request and print the result
resp = kraken_request('/0/private/Balance', {
    "nonce": str(int(1000*time.time()))
}, api_key, api_sec)

# extract the crypto XXMR balance amount from the json response string so we know what amount to wirthdraw
resp_dict = resp.json()
allxmr = (resp_dict['result']['XXMR']) # specify crypto coin

# Construct the request to withdraw all funds of the specified crypto coin to your cold storage and print the result
resp = kraken_request('/0/private/Withdraw', {
    "nonce": str(int(1000*time.time())),
    "asset": "XMR", # specify crypto coin
    "key": "insert wallet name here", #key is the 'name' you choose of your wallet in Kraken, NOT the address of the wallet
    "amount": float(allxmr) # float to convert the balance amout from a string into a number
}, api_key, api_sec)

print(resp.json())