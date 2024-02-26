from aiomisc import Service
from esdbclient import EventStoreDBClient
from esdbclient.streams import CatchupSubscription


class EventStoreWorker(Service):
    _aggregate_root: str
    _esdb: EventStoreDBClient
    _subscription: CatchupSubscription

    def __init__(self, aggregate_root: str, esdb: EventStoreDBClient):
        super().__init__()
        self._aggregate_root = aggregate_root
        self._esdb = esdb

    async def start(self):
        pass

    async def subscribe(self, checkpoint: int = 0):
        self._subscription = self._esdb.subscribe_to_all(filter_include=[fr"^{self._aggregate_root}.*"],
                                                         filter_by_stream_name=True,
                                                         commit_position=checkpoint)

    @property
    def events(self):
        return self._subscription
