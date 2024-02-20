from typing import Optional

from PhotoVote.Event import Event


class ElectionDeleted(Event):
    election_id: Optional[str] = None
