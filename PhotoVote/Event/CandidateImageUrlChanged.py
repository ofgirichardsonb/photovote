from typing import Optional
from Common.Event import Event


class CandidateImageUrlChanged(Event):
    url: Optional[str]
