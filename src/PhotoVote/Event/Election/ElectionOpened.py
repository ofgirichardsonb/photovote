from datetime import datetime

from PhotoVote.Event import Event


class ElectionOpened(Event):
    election_id: str
    open_date: datetime
