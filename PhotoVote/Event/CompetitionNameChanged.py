from typing import Optional
from Common.Event import Event


class CompetitionNameChanged(Event):
    election_id: str
    name: str
