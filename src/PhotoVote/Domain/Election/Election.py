from typing import Optional, Dict, Callable, Type, List

from PhotoVote.Domain import Aggregate
from PhotoVote.Domain.Ballot import BallotId, Ballot
from PhotoVote.Domain.Competition import CompetitionId, Competition
from PhotoVote.Domain.Election import ElectionId, ElectionName, ElectionDescription, ElectionOpenDate, ElectionCloseDate
from PhotoVote.Domain.Voter import Voter, VoterId, VoterName
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from PhotoVote.Event.Candidate import CandidateAdded, CandidateRemoved, CandidateNameChanged, \
    CandidateDescriptionChanged, CandidateImageChanged
from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged
from PhotoVote.Event.Election import ElectionCreated, ElectionDeleted, ElectionNameChanged, \
    ElectionDescriptionChanged, ElectionOpened, ElectionClosed
from PhotoVote.Event.Voter import VoterRegistered
from PhotoVote.Exception import AlreadyVotedError


class Election(Aggregate[ElectionId]):
    name: ElectionName = ElectionName("")
    description: Optional[ElectionDescription] = None
    competitions: List[Competition] = []
    ballots: List[Ballot] = []
    voters: List[Voter] = []
    opened: Optional[ElectionOpenDate] = None
    closed: Optional[ElectionCloseDate] = None
    handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, election_id: ElectionId):
        super().__init__(election_id)
        self.handlers = {
            ElectionCreated: lambda e: self._handle_created(e),
            ElectionDeleted: lambda e: self._handle_deleted(e),
            ElectionNameChanged: lambda e: self._handle_name_changed(e),
            ElectionDescriptionChanged: lambda e: self._handle_description_changed(e),
            ElectionOpened: lambda e: self._handle_opened(e),
            ElectionClosed: lambda e: self._handle_closed(e),
            CompetitionAdded: lambda e: self._handle_competition_added(e),
            CompetitionRemoved: lambda e: self._handle_competition_removed(e),
            CompetitionNameChanged: lambda e: self._handle_competition_name_changed(e),
            CompetitionDescriptionChanged: lambda e: self._handle_competition_description_changed(e),
            CandidateAdded: lambda e: self._handle_candidate_added(e),
            CandidateRemoved: lambda e: self._handle_candidate_removed(e),
            CandidateNameChanged: lambda e: self._handle_candidate_name_changed(e),
            CandidateDescriptionChanged: lambda e: self._handle_candidate_description_changed(e),
            CandidateImageChanged: lambda e: self._handle_candidate_image_changed(e),
            VoterRegistered: lambda e: self._handle_voter_registered(e),
            BallotCreated: lambda e: self._handle_ballot_created(e),
            BallotCandidateRated: lambda e: self._handle_candidate_rated(e),
            BallotCast: lambda e: self._handle_ballot_cast(e),
        }

    def when(self, event: Event) -> None:
        if isinstance(event, tuple(self.handlers.keys())):
            self.handlers[type(event)](event)
        else:
            raise TypeError(f"Unexpected event type: {type(event)} received by Election-{self.id}")

    def ensure_valid_state(self) -> None:
        pass

    def get_competition_by_id(self, cid: CompetitionId) -> Optional[Competition]:
        return next((c for c in self.competitions if c.id == cid), None)

    def _handle_competition_added(self, added: CompetitionAdded) -> None:
        competition = Competition(CompetitionId(added.competition_id))
        competition.apply(added)
        self.competitions.append(competition)

    def _handle_competition_removed(self, removed: CompetitionRemoved) -> None:
        competition = self.get_competition_by_id(CompetitionId(removed.competition_id))
        if competition is not None:
            competition.apply(removed)

    def _handle_competition_name_changed(self, changed: CompetitionNameChanged) -> None:
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_competition_description_changed(self, changed: CompetitionDescriptionChanged) -> None:
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_added(self, added: CandidateAdded) -> None:
        competition = self.get_competition_by_id(CompetitionId(added.competition_id))
        if competition is not None:
            competition.apply(added)

    def _handle_candidate_removed(self, removed: CandidateRemoved) -> None:
        competition = self.get_competition_by_id(CompetitionId(removed.competition_id))
        if competition is not None:
            competition.apply(removed)

    def _handle_candidate_name_changed(self, changed: CandidateNameChanged) -> None:
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_description_changed(self, changed: CandidateDescriptionChanged) -> None:
        competition = self.get_competition_id_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_image_changed(self, changed: CandidateImageChanged) -> None:
        competition = self.get_competition_id_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def get_ballot_by_id(self, bid: BallotId) -> Optional[Ballot]:
        return next((ball for ball in self.ballots if ball.id == bid), None)

    def _handle_candidate_rated(self, rated: BallotCandidateRated) -> None:
        ballot = self.get_ballot_by_id(BallotId(rated.ballot_id))
        if ballot is not None:
            ballot.apply(rated)

    def _handle_ballot_cast(self, cast: BallotCast) -> None:
        ballot = self.get_ballot_by_id(BallotId(cast.ballot_id))
        if ballot is not None:
            ballot.apply(cast)

    def _handle_created(self, created: ElectionCreated) -> None:
        self.id = ElectionId(created.election_id)
        self.name = ElectionName(created.name)
        self.description = ElectionDescription(created.description) if created.description else None

    def _handle_deleted(self, deleted: ElectionDeleted) -> None:
        self.delete()

    def _handle_name_changed(self, changed: ElectionNameChanged) -> None:
        self.name = ElectionName(changed.name)

    def _handle_description_changed(self, changed: ElectionDescriptionChanged) -> None:
        self.description = ElectionDescription(changed.description) if changed.description else None

    def _handle_opened(self, opened: ElectionOpened) -> None:
        self.opened = ElectionOpenDate(opened.open_date)

    def _handle_closed(self, closed: ElectionClosed) -> None:
        self.closed = ElectionCloseDate(closed.close_date)

    def _handle_voter_registered(self, registered: VoterRegistered) -> None:
        voter = Voter(VoterId(registered.voter_id))
        voter.apply(registered)
        for v in self.voters:
            if v.email == voter.email:
                raise AlreadyVotedError()
        self.voters.append(voter)

    def _handle_ballot_created(self, created: BallotCreated) -> None:
        voter = filter(lambda v: v.voter_id == created.voter_id, self.voters)[0]
        if voter is not None:
            if voter.ballot_issued:
                raise AlreadyVotedError()
            voter.apply(created)
            ballot = Ballot(BallotId(created.ballot_id))
            self.ballots.append(ballot)
