from datetime import datetime

from PhotoVote.Event import Event


class ElectionClosed(Event):
    election_id: str
    close_date: datetime
