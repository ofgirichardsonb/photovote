from PhotoVote.Event import Event


class VoterRegistered(Event):
    voter_id: str
    election_id: str
    name: str
    email: str
