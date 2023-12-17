from typing import Optional
from Common.Event import Event


class CandidateDescriptionChanged(Event):
    description: str
