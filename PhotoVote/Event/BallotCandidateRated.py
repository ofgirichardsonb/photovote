from typing import Optional
from Common.Event import Event


class BallotCandidateRated(Event):
    election_id: str
    candidate_id: str
    ballot_id: str
    rating: Optional[int]
