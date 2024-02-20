from typing import Optional

from PhotoVote.Event import Event


class BallotCandidateRated(Event):
    ballot_id: Optional[str] = None
    election_id: Optional[str] = None
    competition_id: Optional[str] = None
    candidate_id: Optional[str] = None
    rating: Optional[int] = None
