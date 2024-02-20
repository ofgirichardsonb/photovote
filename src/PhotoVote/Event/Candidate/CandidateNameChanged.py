from typing import Optional

from PhotoVote.Event import Event


class CandidateNameChanged(Event):
    candidate_id: Optional[str] = None
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    name: Optional[str] = None
