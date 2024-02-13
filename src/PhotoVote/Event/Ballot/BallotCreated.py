from PhotoVote.Event import Event


class BallotCreated(Event):
    ballot_id: str
    voter_id: str
