import os
import requests
from dotenv import load_dotenv


load_dotenv()
TSG_ID = os.environ.get("TSG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_ID = os.environ.get("SECRET_ID")


def create_token():
    url = f"https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token?grant_type=client_credentials&scope:tsg_id:{TSG_ID}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    try:
        token = requests.request(
            "POST", url, headers=headers, auth=(CLIENT_ID, SECRET_ID)
        ).json()
        return token["access_token"]
    except Exception as e:
        print(e)


if __name__ == "__main__":
    token = create_token()
    print(token)
