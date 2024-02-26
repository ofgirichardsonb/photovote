import importlib
import json
from typing import List, Optional, Dict
from uuid import uuid4

from aiomisc import Service
from esdbclient import EventStoreDBClient, RecordedEvent, StreamState, NewEvent
from memphis import Memphis, MemphisError
from memphis.message import Message

from PhotoVote.Domain import AggregateId
from PhotoVote.Domain.Aggregate import BaseAggregate
from PhotoVote.Event import Event
from workers.MemphisWorker import MemphisWorker
from workers.eventstore.Config import Config


class Worker(MemphisWorker):
    # will also validate configuration
    config: Config = Config()
    esdb = EventStoreDBClient(uri=config.eventstore_uri)

    def __init__(self, aggregate_name: str, memphis: Memphis):
        super().__init__(aggregate_name, self._process_events, memphis)

    def _extract_event(self, re: RecordedEvent):
        event_json = re.data.decode('utf-8')
        event_dict = json.loads(event_json)
        event_id = event_dict['id']
        if not event_id:
            raise ValueError("Event id is required")
        event = self._create_event_instance(re.type, event_id, event_dict)
        return event

    async def write_to_eventstore(self, event: Event) -> None:
        try:
            election_id = getattr(event, 'election_id')
            if election_id is None:
                raise ValueError("No election id in event")
            # All events fall under the Election aggregate root. There is no need to also write the
            # other aggregates to their own streams, since they don't stand on their own outside the
            # context of the election to which they belong.
            stream_name = f'Election-{election_id}'
            # There's not much point in loading the event stream since we'll end up just taking the count
            # of items in there as authoritative. Therefore, the fastest approach is to append to the end of the
            # stream blindly. If there were additional validation sources, we could load the aggregate here and
            # do validations here before appending to the stream.
            self.esdb.append_to_stream(stream_name, current_version=StreamState.ANY,
                                       events=[NewEvent(
                                           id=uuid4(),
                                           data=event.model_dump_json().encode('utf8'),
                                           type=event.__class__.__module__)])
        except Exception as ex:
            raise RuntimeError(f"Error: Unable to write to eventstore: {ex}")

    @staticmethod
    def _get_type(class_name: str):
        try:
            package_name, short_name = class_name.rsplit(".", 1)
            package = importlib.import_module(package_name)
            object_type = getattr(package, short_name)
            return object_type
        except ValueError:
            return None

    def _create_event_instance(self, class_name: str, event_id: str, event_dict: Dict) -> Event:
        event_type = self._get_type(class_name)
        event = event_type(id=event_id)
        event = event.model_validate(event_dict)
        return event

    def _create_aggregate_id_instance(self, class_name: str, aggregate_id: str) -> AggregateId:
        aggregate_id_type = self._get_type(class_name)
        aggregate_id = aggregate_id_type(aggregate_id)
        return aggregate_id

    def _create_aggregate_instance(self, class_name: str, aggregate_id: str) -> BaseAggregate:
        aggregate_type = self._get_type(class_name)
        # We assume that the id type is the aggregate type name with `Id` appended
        aid = self._create_aggregate_id_instance(f'{class_name}Id', aggregate_id)
        aggregate = aggregate_type(aid)
        return aggregate

    async def _process_events(self, msgs: List[Message]) -> None:
        for msg in msgs:
            try:
                data = msg.get_data().decode("utf-8")
                obj = json.loads(data)
                if not obj["id"]:
                    raise ValueError("Event id is required")
                headers = msg.get_headers()
                event = self._create_event_instance(headers.get("Event-Type"), obj["id"], obj)
                await self.write_to_eventstore(event)
                await msg.ack()
            except Exception as ex:
                print(ex)
                await msg.nack()
