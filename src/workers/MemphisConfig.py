import os

from dotenv import load_dotenv


class MemphisConfig:
    memphis_host: str
    memphis_account_id: int
    memphis_username: str
    memphis_password: str

    def __init__(self):
        self.memphis_host = os.getenv("MEMPHIS_HOST")
        self.memphis_account_id = int(os.getenv("MEMPHIS_ACCOUNT_ID"))
        self.memphis_username = os.getenv("MEMPHIS_USERNAME")
        self.memphis_password = os.getenv("MEMPHIS_PASSWORD")
