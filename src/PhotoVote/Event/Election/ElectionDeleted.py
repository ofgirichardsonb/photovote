from PhotoVote.Event import Event


class ElectionDeleted(Event):
    election_id: str
