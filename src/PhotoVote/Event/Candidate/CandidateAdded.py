from typing import Optional

from PhotoVote.Event import Event


class CandidateAdded(Event):
    candidate_id: str
    competition_id: str
    election_id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    image_caption: Optional[str]
