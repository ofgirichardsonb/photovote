from typing import Optional

from PhotoVote.Event import Event


class ElectionCreated(Event):
    election_id: str
    name: str
    description: Optional[str]
