from typing import Optional

from PhotoVote.Event import Event


class CandidateDescriptionChanged(Event):
    candidate_id: Optional[str] = None
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    description: Optional[str] = None
