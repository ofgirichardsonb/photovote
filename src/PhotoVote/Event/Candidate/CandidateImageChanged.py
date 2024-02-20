from typing import Optional

from PhotoVote.Event import Event


class CandidateImageChanged(Event):
    candidate_id: Optional[str] = None
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    url: Optional[str] = None
    caption: Optional[str] = None
