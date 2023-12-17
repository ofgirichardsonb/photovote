from Common.Event import Event


class BallotCast(Event):
    election_id: str
