from typing import TypeVar, Generic, Type, Optional

T = TypeVar('T')


class AggregateId(Generic[T]):
    def __init__(self, id_type: Type[T], aggregate_id: Optional[T] = None) -> None:
        self._id_type = id_type
        self._value: T = self._validate_aggregate_id(aggregate_id)

    def _validate_aggregate_id(self, value: Optional[T]) -> T:
        if value is not None and not isinstance(value, self._id_type):
            raise ValueError(f"The value must be an instance of {self._id_type.__name__}")
        return value if value is not None else self._id_type()

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self._value == other._value
