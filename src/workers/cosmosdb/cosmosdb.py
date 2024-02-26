import threading

from aiomisc import entrypoint
from azure.cosmos.aio import CosmosClient
from esdbclient import EventStoreDBClient

from workers.EventStoreWorker import EventStoreWorker
from workers.cosmosdb.Config import Config
from workers.cosmosdb.Worker import Worker

config = Config()
esdb = EventStoreDBClient(uri=config.eventstore_uri)
cosmosdb = CosmosClient(url=config.cosmosdb_endpoint, credential=config.cosmosdb_primary_key)


def start_worker(worker: EventStoreWorker):
    with entrypoint(worker) as loop:
        loop.run_forever()


if __name__ == "__main__":
    election_worker = Worker("Election", esdb, cosmosdb)
    t1 = threading.Thread(target=start_worker, args=[election_worker])
    t1.start()
    t1.join()
