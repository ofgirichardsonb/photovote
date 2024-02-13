from PhotoVote.Event import Event


class BallotCandidateRated(Event):
    ballot_id: str
    election_id: str
    competition_id: str
    candidate_id: str
    rating: int
