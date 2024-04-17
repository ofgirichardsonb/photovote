import os

from dotenv import load_dotenv

from workers.MemphisConfig import MemphisConfig


class Config(MemphisConfig):
    redis_url: str
    keycloak_url: str
    client_id: str
    client_secret: str
    realm_name: str

    def __init__(self):
        load_dotenv()
        super().__init__()
        self.redis_url = os.getenv("REDIS_URL")
        self.keycloak_url = os.getenv("KEYCLOAK_URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.realm_name = os.getenv("REALM_NAME")
