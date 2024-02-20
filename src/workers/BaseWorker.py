from typing import TypeVar, List, Callable, Generic, Coroutine, Any
from uuid import uuid4

from aiomisc import Service
from memphis import Memphis, MemphisError
from memphis.consumer import Consumer
from memphis.message import Message


class BaseWorker(Service):
    _memphis: Memphis
    _consumer: Consumer
    _aggregate_name: str
    # we handle MemphisError here, and we got the context from the caller, so there's no need to send either
    _handler: Callable[[List[Message]], Coroutine[Any, Any, None]]

    def __init__(self,
                 aggregate_name: str,
                 # this is a mouthful, but you are looking for a signature that looks like:
                 # async def process_messages(msgs: List[Message]) -> None
                 handler: Callable[[List[Message]], Coroutine[Any, Any, None]],
                 memphis: Memphis):
        super().__init__()
        self._handler = handler
        self._memphis = memphis
        self._aggregate_name = aggregate_name.lower()

    async def process_messages(self, messages: List[Message], error: MemphisError, context: Any):
        # error will be set in case the last consume() timed out. we don't need to take any action in this case
        # as the consume() has been scheduled periodically in the application startup.
        if not error:
            await self._handler(messages)

    async def start(self):
        await self._memphis.connect(
            host=self.config.memphis_host,
            account_id=self.config.memphis_account_id,
            username=self.config.memphis_username,
            password=self.config.memphis_password,
        )
        consumer_name = f"{self._aggregate_name}-{uuid4()}"
        # self._memphis.consumer() doesn't return Consumer for some reason.
        # noinspection PyTypeChecker
        self._consumer = await self._memphis.consumer(station_name=self._aggregate_name,
                                                      consumer_name=consumer_name,
                                                      batch_size=10,
                                                      batch_max_time_to_wait_ms=1000,
                                                      pull_interval_ms=100,
                                                      consumer_group=self._aggregate_name)
