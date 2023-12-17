from typing import Optional
from ulid import ULID, new as new_ulid, parse as parse_ulid
from Common.Domain import AggregateId


class CandidateId(AggregateId[ULID]):
    @staticmethod
    def generate():
        return CandidateId(new_ulid)

    @staticmethod
    def from_ulid(value: ULID):
        return CandidateId(value)

    @staticmethod
    def from_string(value: str):
        try:
            parsed = parse_ulid(value)
            return CandidateId(parsed)
        except ValueError:
            raise ValueError("Candidate Id must be a valid ULID")

    def __init__(self, aggregate_id: Optional[ULID] = None):
        super().__init__(ULID, aggregate_id)
