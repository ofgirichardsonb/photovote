from typing import Optional

from PhotoVote.Event import Event


class CompetitionAdded(Event):
    competition_id: str
    election_id: str
    name: str
    description: Optional[str]
