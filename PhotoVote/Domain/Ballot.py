from typing import Dict
from ulid import MIN_ULID
from Common.Domain import AggregateRoot
from Common.Event import Event
from PhotoVote.Domain import BallotId, CompetitionId, CandidateId, Rating
from PhotoVote.Event import BallotCandidateRated, BallotCast
from PhotoVote.Exception import AlreadyVotedError


class Ballot(AggregateRoot[BallotId]):
    def __init__(self):
        super().__init__(aggregate_type=BallotId, aggregate_id=BallotId.from_ulid(MIN_ULID))
        self._ratings: Dict[CompetitionId, Dict[CandidateId, Rating]] = {}
        self._is_cast: bool = False

    def when(self, event: Event) -> None:
        if isinstance(event, BallotCandidateRated):
            self._handle_ballot_candidate_rated(event)
        elif isinstance(event, BallotCast):
            self._handle_ballot_cast(event)
        else:
            raise TypeError(f"Unexpected event type: {type(event)}")

    def ensure_valid_state(self) -> None:
        if self._is_cast and len(self._ratings) == 0:
            raise ValueError("Cannot cast an empty ballot")
        if self.id == MIN_ULID or self.id is None:
            raise ValueError("Invalid ULID for Ballot Id")

    def _handle_ballot_candidate_rated(self, event: BallotCandidateRated) -> None:
        if self._is_cast is True:
            raise AlreadyVotedError("Ballot is already cast")
        competition_id = CompetitionId.from_string(event.competition_id)
        candidate_id = CandidateId.from_string(event.candidate_id)

        if event.rating is not None:
            rating = Rating.from_int(event.rating)
            self._update_ratings(competition_id, candidate_id, rating)
        else:
            self._remove_ratings(competition_id, candidate_id)

    def _handle_ballot_cast(self, event: BallotCast) -> None:
        self._is_cast = True

    def _update_ratings(self, competition_id: CompetitionId, candidate_id: CandidateId, rating: Rating):
        self._ratings.setdefault(competition_id, {})
        self._ratings[competition_id][candidate_id] = rating

    def _remove_ratings(self, competition_id, candidate_id):
        if competition_id in self._ratings:
            if candidate_id in self._ratings[competition_id]:
                del self._ratings[competition_id][candidate_id]
            if len(self._ratings[competition_id].items()) == 0:
                del self._ratings[competition_id]
