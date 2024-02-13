from typing import Optional

from PhotoVote.Event import Event


class CandidateDescriptionChanged(Event):
    candidate_id: str
    competition_id: str
    election_id: str
    description: Optional[str]
