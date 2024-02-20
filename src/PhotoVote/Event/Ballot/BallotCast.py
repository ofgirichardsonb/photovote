from typing import Optional

from PhotoVote.Event import Event


class BallotCast(Event):
    ballot_id: Optional[str] = None
