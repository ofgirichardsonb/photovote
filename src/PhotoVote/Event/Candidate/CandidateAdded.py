from typing import Optional

from PhotoVote.Event import Event


class CandidateAdded(Event):
    candidate_id: Optional[str] = None
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    image_caption: Optional[str] = None
