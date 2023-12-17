from typing import Optional
from Common.Event import Event


class CandidateAdded(Event):
    name: str
    election_id: str
    competition_id: str
    description: Optional[str]

