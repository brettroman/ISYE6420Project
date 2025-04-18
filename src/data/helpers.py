from utils.network import api_call
from data.auth import make_auth_url, make_headers

def get_api_data(endpoint, app):
    url = make_auth_url(endpoint, app)
    headers = make_headers(app)
    return api_call(url, headers)