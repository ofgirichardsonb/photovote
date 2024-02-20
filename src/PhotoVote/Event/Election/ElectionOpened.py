from datetime import datetime
from typing import Optional

from PhotoVote.Event import Event


class ElectionOpened(Event):
    election_id: Optional[str] = None
    open_date: Optional[datetime] = None
