from abc import abstractmethod
from typing import Generic, TypeVar, List

from pydantic import BaseModel, model_validator

from PhotoVote.Event import Event
from PhotoVote.Exception import AlreadyDeletedError

T = TypeVar('T')


class BaseAggregate(BaseModel):
    version: int = -1
    deleted: bool = False

    @abstractmethod
    def when(self, event: Event) -> None:
        pass

    @abstractmethod
    def ensure_valid_state(self) -> None:
        pass

    def apply(self, event) -> None:
        if self.deleted:
            raise AlreadyDeletedError()
        self.when(event)
        self.ensure_valid_state()
        self.version = self.version + 1

    def load(self, events: List[Event]) -> None:
        if self.deleted:
            raise AlreadyDeletedError()
        for event in events:
            self.when(event)
            self.version = self.version + 1
        self.ensure_valid_state()

    def delete(self) -> None:
        if self.deleted:
            raise AlreadyDeletedError()
        self.deleted = True


class Aggregate(BaseAggregate, Generic[T]):
    id: T

    @abstractmethod
    def when(self, event: Event) -> None:
        pass

    @abstractmethod
    def ensure_valid_state(self) -> None:
        pass
