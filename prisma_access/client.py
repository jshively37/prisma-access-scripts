import requests
import typing as t

BASE_AUTH_URL = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
BASE_URL = "https://api.sase.paloaltonetworks.com/sse/config/v1"

ENDPOINTS = {"security_rules": "/security-rules"}

HEADERS = {
    "Accept": "application/json",
}

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


class PrismaAccess:
    def __init__(self, tsg_id: str, client_id: str, secret_id: str):
        self.tsg_id = tsg_id
        self.client_id = client_id
        self.secret_id = secret_id

    def create_token(self):
        auth_url = (
            f"{BASE_AUTH_URL}?grant_type=client_credentials&scope:tsg_id:{self.tsg_id}"
        )
        try:
            token = requests.request(
                "POST",
                auth_url,
                headers=AUTH_HEADERS,
                auth=(self.client_id, self.secret_id),
            ).json()
            HEADERS.update({"Authorization": f'Bearer {token["access_token"]}'})
        except Exception as e:
            print(e)

    def make_request(
        self,
        method: str = "GET",
    ):
        pass

    def get_all_security_rules(self):
        url = f"{BASE_URL}/security-rules?position=pre&folder=Mobile%20Users"
        response = requests.get(url, headers=HEADERS).json()
        return response
