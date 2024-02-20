from typing import Optional

from PhotoVote.Event import Event


class ElectionCreated(Event):
    election_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
