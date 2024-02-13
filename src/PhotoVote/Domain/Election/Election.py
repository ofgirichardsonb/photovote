from typing import Optional

from PhotoVote.Domain import AggregateRoot
from PhotoVote.Domain.Ballot import BallotId
from PhotoVote.Domain.Competition import CompetitionId, Competition
from PhotoVote.Domain.Election import ElectionId, ElectionName, ElectionDescription
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from PhotoVote.Event.Candidate import CandidateAdded, CandidateRemoved, CandidateNameChanged, \
    CandidateDescriptionChanged, CandidateImageChanged
from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged
from PhotoVote.Event.Election import ElectionCreated, ElectionDeleted, ElectionNameChanged, ElectionDescriptionChanged, \
    ElectionOpened, ElectionClosed
from PhotoVote.Event.Voter import VoterRegistered


class Election(AggregateRoot[ElectionId]):
    def __init__(self, election_id: ElectionId):
        super().__init__(election_id)

    def when(self, event: Event):
        handlers = {
            ElectionCreated: self._handle_created,
            ElectionDeleted: self._handle_deleted,
            ElectionNameChanged: self._handle_name_changed,
            ElectionDescriptionChanged: self._handle_description_changed,
            ElectionOpened: self._handle_opened,
            ElectionClosed: self._handle_closed,
            CompetitionAdded: self._handle_competition_added,
            CompetitionRemoved: self._handle_competition_removed,
            CompetitionNameChanged: self._handle_competition_name_changed,
            CompetitionDescriptionChanged: self._handle_competition_description_changed,
            CandidateAdded: self._handle_candidate_added,
            CandidateRemoved: self._handle_candidate_removed,
            CandidateNameChanged: self._handle_candidate_name_changed,
            CandidateDescriptionChanged: self._handle_candidate_description_changed,
            CandidateImageChanged: self._handle_candidate_image_changed,
            VoterRegistered: self._handle_voter_registered,
            BallotCreated: self._handle_ballot_created,
            BallotCandidateRated: self._handle_candidate_rated,
            BallotCast: self._handle_ballot_cast,
        }
        handler = handlers.get(type(event))
        if handler:
            handler(event)
        else:
            raise TypeError(f"Unexpected event type: {type(event)} received by Election-{self.id}")

    def ensure_valid_state(self):
        pass

    def get_competition_by_id(self, cid: CompetitionId) -> Optional[Competition]:
        return next((compet for compet in self.competitions if compet.id == cid), None)

    def _handle_competition_added(self, added: CompetitionAdded):
        competition = Competition(CompetitionId(added.competition_id))
        competition.apply(added)
        self.competitions.append(competition)

    def _handle_competition_removed(self, removed: CompetitionRemoved):
        competition = self.get_competition_by_id(CompetitionId(removed.competition_id))
        if competition is not None:
            competition.apply(removed)

    def _handle_competition_name_changed(self, changed: CompetitionNameChanged):
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_competition_description_changed(self, changed: CompetitionDescriptionChanged):
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_added(self, added: CandidateAdded):
        competition = self.get_competition_by_id(CompetitionId(added.competition_id))
        if competition is not None:
            competition.apply(added)

    def _handle_candidate_removed(self, removed: CandidateRemoved):
        competition = self.get_competition_by_id(CompetitionId(removed.competition_id))
        if competition is not None:
            competition.apply(removed)

    def _handle_candidate_name_changed(self, changed: CandidateNameChanged):
        competition = self.get_competition_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_description_changed(self, changed: CandidateDescriptionChanged):
        competition = self.get_competition_id_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)

    def _handle_candidate_image_changed(self, changed: CandidateImageChanged):
        competition = self.get_competition_id_by_id(CompetitionId(changed.competition_id))
        if competition is not None:
            competition.apply(changed)


    def get_ballot_by_id(self, bid: BallotId) -> Optional['Ballot']:
        return next((ball for ball in self.ballots if ball.id == bid), None)

    def _handle_candidate_rated(self, rated: BallotCandidateRated):
        ballot = self.get_ballot_by_id(BallotId(rated.ballot_id))
        if ballot is not None:
            ballot.apply(rated)

    def _handle_ballot_cast(self, cast: BallotCast):
        ballot = self.get_ballot_by_id(BallotId(cast.ballot_id))
        if ballot is not None:
            ballot.apply(cast)

    def _handle_created(self, created: ElectionCreated):
        self.id = ElectionId(created.election_id)
        self.name = ElectionName(created.name)
        self.description = ElectionDescription(created.description) if created.description else None

    def _handle_deleted(self, deleted: ElectionDeleted):
        self.delete()

    def _handle_name_changed(self, changed: ElectionNameChanged):
        self.name = ElectionName(changed.name)

    def _handle_description_changed(self, changed: ElectionDescriptionChanged):
        self.description = ElectionDescription(changed.description) if changed.description else None
