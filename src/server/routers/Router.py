from typing import List, Optional

from memphis import Memphis, Headers
from memphis.producer import Producer
from uuid import uuid4

from PhotoVote.Event import Event
import os


class Router:
    _name: str
    _stations: List[str]
    _producer: Optional[Producer] = None

    def __init__(self, name: str, stations: List[str]):
        self._name = name
        self._stations = stations
        self._memphis: Memphis = Memphis()

    async def publish_event(self, event: Event):
        if self._producer is None:
            memphis: Memphis = Memphis()
            str_acct_id = os.getenv('MEMPHIS_ACCOUNT_ID')
            account_id = 0
            host = os.getenv('MEMPHIS_HOST') or ''
            username = os.getenv('MEMPHIS_USERNAME') or ''
            password = os.getenv('MEMPHIS_PASSWORD') or ''
            if str_acct_id is not None:
                account_id = int(str_acct_id)
            await memphis.connect(
                host=host,
                username=username,
                password=password,
                account_id=account_id
            )
            for station in self._stations:
                await memphis.station(station)
            self._producer = await memphis.producer(self._stations, f'{self._name}-{uuid4()}')
        headers = Headers()
        headers.add('Event-Type', event.__class__.__module__)
        await self._producer.produce(message=event.model_dump(), headers=headers)
