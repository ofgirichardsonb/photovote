from typing import Optional

from PhotoVote.Event import Event


class CompetitionDescriptionChanged(Event):
    competition_id: Optional[str] = None
    election_id: Optional[str] = None
    description: Optional[str] = None
