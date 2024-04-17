from typing import TypeVar, List, Callable, Generic, Coroutine, Any, Awaitable, Optional
from uuid import uuid4

import asyncio
from aiomisc import Service
from memphis import Memphis, MemphisError
from memphis.consumer import Consumer
from memphis.message import Message

from workers.MemphisConfig import MemphisConfig


class MemphisWorker(Service):
    _memphis: Memphis
    _consumer: Consumer
    _station_name: str
    # we handle MemphisError here, and we got the context from the caller, so there's no need to send either
    _handler: Callable[[List[Message], Optional[MemphisError], dict], Awaitable[None]]
    _config: MemphisConfig

    def __init__(self,
                 station_name: str,
                 # this is a mouthful, but you are looking for a signature that looks like:
                 # async def process_messages(msgs: List[Message]) -> None
                 handler: Callable[[List[Message], Optional[MemphisError], dict], Awaitable[None]],
                 memphis: Memphis,
                 config: MemphisConfig):
        super().__init__()
        self._handler = handler
        self._memphis = memphis
        self._station_name = station_name.lower()
        self._config = config

    async def process_messages(self, messages: List[Message], error: MemphisError, context: dict):
        # error will be set in case the last consume() timed out. we don't need to take any action in this case
        # as the consume() has been scheduled periodically in the application startup.
        if not error and messages.__len__() > 0:
            await self._handler(messages, error, context)

    async def start(self):
        await self._memphis.connect(
            host=self._config.memphis_host,
            account_id=self._config.memphis_account_id,
            username=self._config.memphis_username,
            password=self._config.memphis_password,
        )
        consumer_name = f"{self._station_name}-{uuid4()}"
        # self._memphis.consumer() doesn't return Consumer for some reason.
        # noinspection PyTypeChecker
        self._consumer = await self._memphis.consumer(station_name=self._station_name,
                                                      consumer_name=consumer_name,
                                                      batch_size=10,
                                                      batch_max_time_to_wait_ms=1000,
                                                      pull_interval_ms=100,
                                                      consumer_group=self._station_name)
        while True:
            self._consumer.consume(self.process_messages)
            await asyncio.sleep(1)
