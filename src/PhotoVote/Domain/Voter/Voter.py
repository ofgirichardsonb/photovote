from typing import Callable, Type, Dict

from PhotoVote.Domain import Aggregate, AggregateId
from PhotoVote.Domain.Voter import VoterId, VoterName, VoterEmail
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated
from PhotoVote.Event.Voter import VoterRegistered


class Voter(Aggregate[VoterId]):
    name: VoterName
    email: VoterEmail
    ballot_issued: bool = False
    _handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._handlers = {
            VoterRegistered: lambda e: self._handle_registered(e),
            BallotCreated: lambda e: self._handle_ballot_created(e)
        }

    def when(self, event: Event) -> None:
        if isinstance(event, tuple(self._handler.keys())):
            self._handler[type(event)](event)
        else:
            raise TypeError(f"Unknown event: {type(event)} received by Voter-{self.id}")

    def ensure_valid_state(self) -> None:
        if not isinstance(self.id, VoterId):
            raise TypeError("Voter id must be of type VoterId")
        if self.id == AggregateId.empty():
            raise ValueError("Voter id must not be the empty ULID")
        if self.name == "":
            raise ValueError("Voter name must not be empty")
        if self.email == "":
            raise ValueError("Voter email must not be empty")

    def _handle_registered(self, registered: VoterRegistered) -> None:
        self.id = VoterId(registered.voter_id)
        self.name = VoterName(registered.name)
        self.email = VoterEmail(registered.email)

    def _handle_ballot_created(self, created: BallotCreated) -> None:
        self.ballot_issued = True
