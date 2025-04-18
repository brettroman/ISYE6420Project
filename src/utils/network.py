import requests

def api_call(endpoint, headers):
    return requests.get(endpoint, headers=headers).json()