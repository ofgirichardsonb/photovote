from PhotoVote.Event import Event


class CompetitionNameChanged(Event):
    competition_id: str
    election_id: str
    name: str
