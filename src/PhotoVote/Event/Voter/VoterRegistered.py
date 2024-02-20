from typing import Optional

from PhotoVote.Event import Event


class VoterRegistered(Event):
    voter_id: Optional[str]
    election_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
