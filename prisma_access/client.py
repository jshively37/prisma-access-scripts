import requests

# import typing as t

BASE_AUTH_URL = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
BASE_URL = "https://api.sase.paloaltonetworks.com/sse/config/v1"

ENDPOINTS = {"security_rules": "/security-rules", "decryption": "/decryption-rules"}

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

REQUEST_TYPES = {"security_rules": "security_rules", "decryption": "decryption"}


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

    def _make_request(
        self, endpoint: str, headers: str = HEADERS, method: str = "GET", data: str = ""
    ):
        """Function that is used for making API requests.

        Args:
            endpoint (str): Path to target against. Will be combined with BASE_URL to form full URL
            headers (str, optional): Headers to use. Defaults to HEADERS.
            method (str, optional): HTTP Verb. Defaults to "GET".
            data (str, optional): Payload. Defaults to "".

        Returns:
            JSON: returns the output from the URL request
        """
        url = BASE_URL + endpoint
        return requests.request(
            method=method, url=url, headers=HEADERS, data=data
        ).json()

    def _loop_all_folders(self, endpoint, request_type):
        """Function that will loop all folders and positions and returns a list of dictionaries

        Args:
            endpoint str: Endpoint to target from the ENDPOINTS dictionary
            request_type str: Type of request to target from REQUEST_TYPES dictionary. This
                            builds the value that will be passed to the dictionary for the
                            data that was returned from the response.

        Returns:
            _type_: List of dictionaries
        """
        list_to_return = []
        for folder in FOLDERS:
            if folder != "Service Connections":
                for position in POSITIONS:
                    _ = {}
                    full_endpoint = f"{endpoint}?position={position}&folder={folder}"
                    print(full_endpoint)
                    print(folder, position)
                    response = self._make_request(endpoint=full_endpoint)
                    print(response)
                    _ |= {
                        "folder": folder,
                        "position": position,
                        f"{request_type}": response["data"],
                    }
                    list_to_return.append(_)
        return list_to_return

    def get_all_security_rules(self):
        """Retrieve all security rules from all folders and positions.

        Returns:
            Dict: List of dictionaries containing the data, folder, and position.
        """
        return self._loop_all_folders(
            endpoint=ENDPOINTS["security_rules"],
            request_type=REQUEST_TYPES["security_rules"],
        )

    def get_all_decryption_rules(self):
        """Retrieve all decryption rules from all folders and positions.

        Returns:
            Dict: List of dictionaries containing the data, folder, and position.
        """
        return self._loop_all_folders(
            endpoint=ENDPOINTS["decryption"], request_type=REQUEST_TYPES["decryption"]
        )

    def get_single_security_rule(self, folder: str, position: str = "pre"):
        """Retrieve rules for only folder and position in Prisma Access

        Args:
            folder (str): Folder to target
            position (str, optional): Location of the rule. Defaults to "pre".

        Returns:
            _type_: A dictionary containing the folder, position, and security rule data.
        """
        rule_dict = {}
        endpoint = f"/{ENDPOINTS['security_rules']}?position={position}&folder={folder}"
        response = self._make_request(endpoint=endpoint)
        rule_dict |= {
            "folder": folder,
            "position": position,
            "security_rules": response["data"],
        }
        return rule_dict
