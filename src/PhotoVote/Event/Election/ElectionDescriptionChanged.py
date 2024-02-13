from typing import Optional

from PhotoVote.Event import Event


class ElectionDescriptionChanged(Event):
    election_id: str
    description: Optional[str]

