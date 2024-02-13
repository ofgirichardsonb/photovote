from __future__ import annotations
import ulid
from pydantic import RootModel
from ulid import parse as parse_ulid


class AggregateId(RootModel):
    @classmethod
    def empty(cls) -> str:
        return str(ulid.from_int(0))

    def __init__(self, aggregate_id: str):
        try:
            parse_ulid(aggregate_id)
        except ValueError:
            raise ValueError("Aggregate ID must be a valid ULID")
        self.root = aggregate_id

    def __str__(self):
        return self.root
