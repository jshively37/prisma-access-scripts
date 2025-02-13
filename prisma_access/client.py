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

FOLDERS = [
    "Shared",
    "Mobile Users",
    "Remote Networks",
    "Service Connections",
    "Mobile Users Container",
    "Mobile Users Explicit Proxy",
]

POSITIONS = ["pre", "post"]


class PrismaAccess:
    def __init__(self, tsg_id: str, client_id: str, secret_id: str):
        """Init function

        Args:
            tsg_id (str): TSG ID
            client_id (str): CLIENT ID
            secret_id (str): SECRET ID
        """
        self.tsg_id = tsg_id
        self.client_id = client_id
        self.secret_id = secret_id

    def create_token(self):
        """Function that handles authenticating to Prisma Access and retrieving the token."""
        auth_url = (
            f"{BASE_AUTH_URL}?grant_type=client_credentials&scope:tsg_id:{self.tsg_id}"
        )
        try:
            token = requests.request(
                method="POST",
                url=auth_url,
                headers=AUTH_HEADERS,
                auth=(self.client_id, self.secret_id),
            ).json()
            HEADERS.update({"Authorization": f'Bearer {token["access_token"]}'})
        except Exception as e:
            print(e)

    def make_request(
        self, url: str, headers: str = HEADERS, method: str = "GET", data: str = ""
    ):
        """Function that is used for making API requests.

        Args:
            url (str): URL to target
            headers (str, optional): Headers to use. Defaults to HEADERS.
            method (str, optional): HTTP Verb. Defaults to "GET".
            data (str, optional): Payload. Defaults to "".

        Returns:
            JSON: returns the output from the URL request
        """
        return requests.request(
            method=method, url=url, headers=HEADERS, data=data
        ).json()

    def get_all_security_rules(self):
        """Retrieve all security rules from all folders and positions.

        Returns:
            Dict: List of dictionaries containing the data, folder, and position.
        """
        all_rules_list = []
        for folder in FOLDERS:
            rule_dict = {}
            # Skip service connections because we don't do security processing on those nodes.
            if folder == "Service Connections":
                pass
            else:
                for position in POSITIONS:
                    url = (
                        f"{BASE_URL}/security-rules?position={position}&folder={folder}"
                    )
                    response = self.make_request(url=url)
                    rule_dict.update(
                        {
                            "folder": folder,
                            "position": position,
                            "security_rules": response["data"],
                        }
                    )
                    all_rules_list.append(rule_dict)
        return all_rules_list
