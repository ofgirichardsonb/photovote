import os

from dotenv import load_dotenv


class EventStoreConfig:
    eventstore_uri: str
    memphis_host: str
    memphis_account_id: int
    memphis_username: str
    memphis_password: str

    def __init__(self):
        load_dotenv(".env")
        self.eventstore_uri = os.getenv("EVENTSTORE_URI")
        if not self.eventstore_uri:
            raise EnvironmentError("Event Store DB URI was not provided")
        self.memphis_host = os.getenv("MEMPHIS_HOST")
        if not self.memphis_host:
            raise EnvironmentError("Memphis host was not provided")
        memphis_account_id = os.getenv("MEMPHIS_ACCOUNT_ID")
        if not memphis_account_id:
            raise EnvironmentError("Memphis account id was not provided")
        try:
            self.memphis_account_id = int(memphis_account_id)
        except ValueError:
            raise EnvironmentError("Invalid Memphis account id")
        self.memphis_username = os.getenv("MEMPHIS_USERNAME")
        if not self.memphis_username:
            raise EnvironmentError("Memphis username was not provided")
        self.memphis_password = os.getenv("MEMPHIS_PASSWORD")
        if not self.memphis_password:
            raise EnvironmentError("Memphis password was not provided")
