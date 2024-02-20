from typing import Optional

from PhotoVote.Event import Event


class CompetitionRemoved(Event):
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
