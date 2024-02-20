from datetime import datetime
from typing import Optional

from PhotoVote.Event import Event


class ElectionClosed(Event):
    election_id: Optional[str] = None
    close_date: Optional[datetime] = None

