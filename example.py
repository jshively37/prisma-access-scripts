import os
from dotenv import load_dotenv
from pprint import pprint as pp

from prisma_access.client import PrismaAccess

load_dotenv()
TSG_ID = os.environ.get("TSG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_ID = os.environ.get("SECRET_ID")


if __name__ == "__main__":
    client = PrismaAccess(tsg_id=TSG_ID, client_id=CLIENT_ID, secret_id=SECRET_ID)
    client.create_token()
    resp = client.get_all_security_rules()
    print(resp)
