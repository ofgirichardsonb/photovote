from typing import Optional
from ulid import ULID, new as new_ulid, parse as parse_ulid
from Common.Domain import AggregateId


class CompetitionId(AggregateId[ULID]):
    @staticmethod
    def generate():
        return CompetitionId(new_ulid)

    @staticmethod
    def from_ulid(value: ULID):
        return CompetitionId(value)

    @staticmethod
    def from_string(value: str):
        try:
            parsed = parse_ulid(value)
            return CompetitionId(parsed)
        except ValueError:
            raise ValueError("Competition Id must be a valid ULID")

    def __init__(self, aggregate_id: Optional[ULID] = None):
        super().__init__(ULID, aggregate_id)
