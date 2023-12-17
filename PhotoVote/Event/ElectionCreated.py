from typing import Optional
from Common.Event import Event


class ElectionCreated(Event):
    name: str
    description: Optional[str]
