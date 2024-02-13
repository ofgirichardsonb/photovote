from typing import Dict

from pydantic import Field

from PhotoVote.Domain import AggregateRoot, AggregateId
from PhotoVote.Domain.Ballot import BallotId, Rating
from PhotoVote.Domain.Candidate import CandidateId
from PhotoVote.Domain.Competition import CompetitionId
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from PhotoVote.Exception import AlreadyVotedError


class Ballot(AggregateRoot[BallotId]):
    ratings: Dict[CompetitionId, Dict[CandidateId, Rating]] = Field(default_factory=lambda: {})
    cast: bool = False

    def __init__(self, ballot_id: BallotId):
        super().__init__(ballot_id)

    def when(self, event: Event):
        if isinstance(event, BallotCreated):
            self._handle_created(event)
        elif isinstance(event, BallotCandidateRated):
            self._handle_candidate_rated(event)
        elif isinstance(event, BallotCast):
            self._handle_cast(event)
        else:
            raise ValueError(f"Unknown event type {event.__class__.__name__}")

    def ensure_valid_state(self):
        if not isinstance(self.id, BallotId):
            raise ValueError("Ballot id must be of type BallotId")
        if self.id == AggregateId.empty():
            raise ValueError("Ballot ID cannot be empty")

    def _handle_created(self, created: BallotCreated):
        self.id = BallotId(created.ballot_id)

    def _handle_candidate_rated(self, rated: BallotCandidateRated):
        if self.cast:
            raise AlreadyVotedError()
        if rated.competition_id not in self.ratings:
            self.ratings[rated.competition_id] = {}
        self.ratings[rated.competition_id][rated.candidate_id] = rated.rating

    def _handle_cast(self, cast: BallotCast):
        if self.cast:
            raise AlreadyVotedError()
        self.cast = True
