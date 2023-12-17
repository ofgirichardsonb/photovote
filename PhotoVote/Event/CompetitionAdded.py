from typing import Optional
from Common.Event import Event


class CompetitionAdded(Event):
    election_id: str
    name: str
    description: Optional[str]