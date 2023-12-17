from typing import TypeVar, Generic, Type, List
from Common.Exception import AlreadyDeletedError
from Common.Event import Event

T = TypeVar("T")


class AggregateRoot(Generic[T]):
    def __init__(self, aggregate_type: Type[T], aggregate_id: T):
        self._aggregate_type: Type[T] = aggregate_type
        self._aggregate_id: T = aggregate_id
        self._version: int = -1
        self._deleted: bool = False

    @property
    def id(self) -> T:
        return self._aggregate_id

    @property
    def deleted(self) -> bool:
        return self._deleted

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, version: int) -> None:
        self._version = version

    def when(self, event: Event) -> None:
        pass

    def ensure_valid_state(self):
        pass

    def apply(self, event: Event) -> None:
        if self.deleted:
            raise AlreadyDeletedError("%s-%s is already deleted" % (self._aggregate_type, self._aggregate_id))
        self.when(event)
        self.ensure_valid_state()
        self.version += 1

    def load(self, history: List[Event]) -> None:
        for event in history:
            self.when(event)
            self.version += 1

    def delete(self):
        if self.deleted:
            raise AlreadyDeletedError("%s-%s is already deleted" % (self._aggregate_type, self._aggregate_id))
        self._deleted = True
