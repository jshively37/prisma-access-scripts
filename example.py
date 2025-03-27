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
    # all_rules = client.get_all_security_rules()
    # pp(all_rules)
    # print("*" * 50)
    # print("*" * 50)
    # single_rule = client.get_single_security_rule(folder="Mobile Users", position="pre")
    # pp(single_rule)
    # print("*" * 50)
    # print("*" * 50)
    # all_decrypt_rules = client.get_all_decryption_rules()
    # pp(all_decrypt_rules)
    # client.configure_adem()
    all_address_objects = client.get_all_address_objects()
    print(all_address_objects)
