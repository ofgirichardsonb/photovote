from PhotoVote.Event import Event


class CandidateRemoved(Event):
    candidate_id: str
    competition_id: str
    election_id: str
