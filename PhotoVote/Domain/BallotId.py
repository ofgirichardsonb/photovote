from __future__ import annotations
from ulid import ULID, new as new_ulid, parse as parse_ulid, MIN_ULID
from typing import Optional

from Common import AggregateId


class BallotId(AggregateId):
    @staticmethod
    def empty() -> BallotId:
        return BallotId(MIN_ULID)

    @staticmethod
    def generate():
        return BallotId(new_ulid)

    @staticmethod
    def from_ulid(value: ULID):
        return BallotId(value)

    @staticmethod
    def from_string(value: str):
        try:
            parsed = parse_ulid(value)
            return BallotId(parsed)
        except ValueError:
            raise ValueError("Ballot Id must be a valid ULID")

    def __init__(self, aggregate_id: Optional[ULID] = None) -> None:
        super().__init__(ULID, aggregate_id)
