from typing import Optional

from PhotoVote.Event import Event


class CompetitionDescriptionChanged(Event):
    competition_id: str
    election_id: str
    description: Optional[str]
