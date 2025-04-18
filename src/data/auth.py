from project.config import auth_config
from project.logger import logger

def make_auth_url(endpoint, app):
    if app == "sportsdata":
        return f"{endpoint}?key={auth_config.get(app).get("key")}"

def make_headers(app):
    headers = {}
    if app == "sportsdata":
        headers = {
            "Ocp-Apim-Subscription-Key": f"{auth_config.get(app).get("key")}"
        }

    return headers

