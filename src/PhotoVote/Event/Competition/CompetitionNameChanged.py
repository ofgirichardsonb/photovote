from typing import Optional

from PhotoVote.Event import Event


class CompetitionNameChanged(Event):
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    name: Optional[str] = None
