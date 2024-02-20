from typing import Optional

from PhotoVote.Event import Event


class BallotCreated(Event):
    ballot_id: Optional[str] = None
    voter_id: Optional[str] = None
