from PhotoVote.Domain import AggregateRoot, AggregateId
from PhotoVote.Domain.Voter import VoterId, VoterName, VoterEmail
from PhotoVote.Event import Event
from PhotoVote.Event.Voter import VoterRegistered


class Voter(AggregateRoot[VoterId]):
    name: VoterName
    email: VoterEmail

    def __init__(self, voter_id: VoterId):
        super().__init__(voter_id)

    def when(self, event: Event):
        if isinstance(event, VoterRegistered):
            self._handle_registered(event)
        else:
            raise TypeError(f"Unknown event: {type(event)} received by Voter-{self.id}")

    def ensure_valid_state(self):
        if not isinstance(self.id, VoterId):
            raise TypeError("Voter id must be of type VoterId")
        if self.id == AggregateId.empty():
            raise ValueError("Voter id must not be the empty ULID")
        if self.name == "":
            raise ValueError("Voter name must not be empty")
        if self.email == "":
            raise ValueError("Voter email must not be empty")

    def _handle_registered(self, registered: VoterRegistered):
        self.id = VoterId(registered.voter_id)
        self.name = VoterName(registered.name)
        self.email = VoterEmail(registered.email)
