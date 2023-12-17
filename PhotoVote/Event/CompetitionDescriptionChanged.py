from typing import Optional
from Common.Event import Event


class CompetitionDescriptionChanged(Event):
    election_id: str
    description: Optional[str]
