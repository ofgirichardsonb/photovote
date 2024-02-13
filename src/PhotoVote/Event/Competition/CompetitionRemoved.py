from PhotoVote.Event import Event


class CompetitionRemoved(Event):
    competition_id: str
    election_id: str
