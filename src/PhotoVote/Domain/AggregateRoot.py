from abc import abstractmethod
from typing import Generic, TypeVar, List

from pydantic import BaseModel

from PhotoVote.Event import Event
from PhotoVote.Exception import AlreadyDeletedError

T = TypeVar('T')


class AggregateRoot(BaseModel, Generic[T]):
    id: T
    version: int = -1
    deleted: bool = False

    @abstractmethod
    def when(self, event: Event):
        pass

    @abstractmethod
    def ensure_valid_state(self):
        pass

    def apply(self, event):
        if self.deleted:
            raise AlreadyDeletedError()
        self.when(event)
        self.ensure_valid_state()
        self.version = self.version + 1

    def load(self, events: List[Event]):
        if self.deleted:
            raise AlreadyDeletedError()
        for event in events:
            self.when(event)
            self.version = self.version + 1
        self.ensure_valid_state()

    def delete(self):
        if self.deleted:
            raise AlreadyDeletedError()
        self.deleted = True

    def __init__(self, aggregate_id: T):
        self.id = aggregate_id
