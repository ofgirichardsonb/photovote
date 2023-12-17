from Common.Event import Event


class CandidateRemoved(Event):
    election_id: str
    competition_id: str
