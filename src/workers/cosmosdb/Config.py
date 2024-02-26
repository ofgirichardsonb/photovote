import os

from dotenv import load_dotenv


class Config:
    eventstore_uri: str
    cosmosdb_endpoint: str
    cosmosdb_primary_key: str

    def __init__(self):
        load_dotenv(".env")
        self.eventstore_uri = os.getenv("EVENTSTORE_URI")
        if not self.eventstore_uri:
            raise EnvironmentError("EventStore URI was not provided")
        self.cosmosdb_endpoint = os.getenv("COSMOSDB_ENDPOINT")
        if not self.cosmosdb_endpoint:
            raise EnvironmentError("CosmosDB account name was not provided")
        self.cosmosdb_primary_key = os.getenv("COSMOSDB_PRIMARY_KEY")
        if not self.cosmosdb_primary_key:
            raise EnvironmentError("CosmosDB primary key was not provided")
