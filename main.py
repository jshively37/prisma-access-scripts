import os
import requests
from dotenv import load_dotenv
from pprint import pprint as pp


load_dotenv()
TSG_ID = os.environ.get("TSG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_ID = os.environ.get("SECRET_ID")

BASE_URL = 'https://api.sase.paloaltonetworks.com/sse/config/v1'

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}

HEADERS = {
  'Accept': 'application/json',
}


def create_token():
    url = f"https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope:tsg_id:{TSG_ID}"
    try:
        token = requests.request(
            "POST", url, headers=AUTH_HEADERS, auth=(CLIENT_ID, SECRET_ID)
        ).json()
        return HEADERS.update({'Authorization': f'Bearer {token["access_token"]}'})
    except Exception as e:
        print(e)

def get_security_rules():
    url = f"{BASE_URL}/security-rules?position=pre&folder=Mobile%20Users"
    response = requests.get(url, headers=HEADERS).json()
    pp(response)


if __name__ == "__main__":
    token = create_token()
    get_security_rules()
