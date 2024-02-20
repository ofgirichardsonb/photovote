from typing import Optional

from PhotoVote.Event import Event


class ElectionNameChanged(Event):
    election_id: Optional[str] = None
    name: Optional[str] = None
