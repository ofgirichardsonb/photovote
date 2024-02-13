from PhotoVote.Event import Event


class ElectionNameChanged(Event):
    election_id: str
    name: str
