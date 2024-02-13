from typing import Optional

from PhotoVote.Event import Event


class CandidateImageChanged(Event):
    candidate_id: str
    competition_id: str
    election_id: str
    url: Optional[str]
    caption: Optional[str]
