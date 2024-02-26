import importlib
import json
from typing import Dict, Optional, Type

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from esdbclient import EventStoreDBClient, RecordedEvent

from PhotoVote.Event import Event
from workers.EventStoreWorker import EventStoreWorker
from workers.cosmosdb.handlers.Handler import Handler


class Worker(EventStoreWorker):
    _aggregate_root: str
    _container: ContainerProxy
    _checkpoints: ContainerProxy
    _handler: Optional[Handler] = None

    def __init__(self, aggregate_root: str, esdb: EventStoreDBClient, cosmosdb: CosmosClient):
        super().__init__(aggregate_root, esdb)
        self._aggregate_root = aggregate_root
        self._cosmosdb = cosmosdb

    @staticmethod
    def _get_type(class_name: str) -> Optional[Type]:
        try:
            package_name, short_name = class_name.rsplit(".", 1)
            package = importlib.import_module(package_name)
            object_type = getattr(package, short_name)
            return object_type
        except ValueError:
            return None
        except TypeError:
            return None

    def _create_event_instance(self, class_name: str, event_json: str) -> Optional[Event]:
        event_type = self._get_type(class_name)
        if event_type:
            event_dict = json.loads(event_json)
            event_id = event_dict['id']
            if not event_id:
                raise ValueError("Invalid event JSON: no event id provided")
            event = event_type(id=event_id)
            event = event.model_validate(event_dict)
            return event
        print(f"WARNING: Unknown event type '{event_type}' received from EventStore")
        return None

    async def start(self):
        db = await self._cosmosdb.create_database_if_not_exists("PhotoVote")
        self._container = await db.create_container_if_not_exists(self._aggregate_root,
                                                                  partition_key=PartitionKey(path="/id"))
        self._handler = Handler(self._container)
        self._checkpoints = await db.create_container_if_not_exists("checkpoints",
                                                                    partition_key=PartitionKey(path="/id"))
        commit_position = 0
        try:
            checkpoint = await self._checkpoints.read_item(self._aggregate_root, self._aggregate_root)
            commit_position = int(checkpoint["commit_position"])
        except CosmosResourceNotFoundError as ex:
            await self._checkpoints.upsert_item({"id": self._aggregate_root, "commit_position": 0})
        await self.subscribe(commit_position)
        for event in self.events:
            await self.process_event(event)

    async def process_event(self, re: RecordedEvent):
        event_json = re.data.decode("utf-8")
        event = self._create_event_instance(re.type, event_json)
        if event:
            await self._handler.handle(event)
            await self._checkpoints.upsert_item({"id": self._aggregate_root, "commit_position": re.commit_position})

