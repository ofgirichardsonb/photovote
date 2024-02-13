from PhotoVote.Event import Event


class CandidateNameChanged(Event):
    candidate_id: str
    competition_id: str
    election_id: str
    name: str
