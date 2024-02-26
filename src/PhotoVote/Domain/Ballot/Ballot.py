from typing import Dict, Type, Callable

from pydantic import Field

from PhotoVote.Domain import Aggregate, AggregateId
from PhotoVote.Domain.Ballot import BallotId, Rating
from PhotoVote.Domain.Candidate import CandidateId
from PhotoVote.Domain.Competition import CompetitionId
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from PhotoVote.Exception import AlreadyVotedError


class Ballot(Aggregate[BallotId]):
    ratings: Dict[CompetitionId, Dict[CandidateId, Rating]] = Field(default_factory=lambda: {})
    cast: bool = False
    _handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._handlers = {
            BallotCreated: lambda e: self._handle_created(e),
            BallotCandidateRated: lambda e: self._handle_candidate_rated(e),
            BallotCast: lambda e: self._handle_cast(e)
        }

    def when(self, event: Event) -> None:
        if isinstance(event, tuple(self._handlers.keys())):
            self._handlers[type(event)](event)
        else:
            raise ValueError(f"Unknown event type {event.__class__.__name__}")

    def ensure_valid_state(self) -> None:
        if not isinstance(self.id, BallotId):
            raise ValueError("Ballot id must be of type BallotId")
        if self.id == AggregateId.empty():
            raise ValueError("Ballot ID cannot be empty")

    def _handle_created(self, created: BallotCreated) -> None:
        self.id = BallotId(created.ballot_id)

    def _handle_candidate_rated(self, rated: BallotCandidateRated) -> None:
        if self.cast:
            raise AlreadyVotedError()
        competition_id = CompetitionId(rated.competition_id) if rated.competition_id else None
        candidate_id = CandidateId(rated.candidate_id) if rated.candidate_id else None
        rating = Rating(rated.rating) if (0 < rated.rating <= 5) else None
        if competition_id is None:
            raise ValueError("Competition id is required")
        if candidate_id is None:
            raise ValueError("Candidate id is required")
        if rating is None:
            raise ValueError("Rating must be between 1 and 5")
        if competition_id not in self.ratings:
            self.ratings[competition_id] = {}
        self.ratings[competition_id][candidate_id] = rating

    def _handle_cast(self, cast: BallotCast) -> None:
        if self.cast:
            raise AlreadyVotedError()
        self.cast = True
