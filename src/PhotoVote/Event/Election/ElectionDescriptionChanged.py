from typing import Optional

from PhotoVote.Event import Event


class ElectionDescriptionChanged(Event):
    election_id: Optional[str] = None
    description: Optional[str] = None

