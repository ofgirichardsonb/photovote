from typing import Optional

from PhotoVote.Event import Event


class BallotCreated(Event):
    election_id: Optional[str] = None
    ballot_id: Optional[str] = None
    voter_id: Optional[str] = None
