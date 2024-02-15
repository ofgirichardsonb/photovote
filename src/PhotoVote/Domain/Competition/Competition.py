from typing import Optional, List

from pydantic import Field

from PhotoVote.Domain import AggregateRoot, AggregateId
from PhotoVote.Domain.Candidate import Candidate, CandidateName, CandidateDescription, CandidateImage, ImageUrl, \
    ImageCaption, CandidateId
from PhotoVote.Domain.Competition import CompetitionId, CompetitionName, CompetitionDescription
from PhotoVote.Event import Event
from PhotoVote.Event.Candidate import CandidateAdded, CandidateNameChanged, CandidateDescriptionChanged, \
    CandidateImageChanged, CandidateRemoved
from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged


class Competition(AggregateRoot[CompetitionId]):
    name: CompetitionName = CompetitionName("")
    description: Optional[CompetitionDescription] = None
    candidates: List[Candidate] = Field(default_factory=lambda: [])

    def __init__(self, competition_id: CompetitionId):
        super().__init__(competition_id)

    def when(self, event: Event):
        if isinstance(event, CompetitionAdded):
            self._handle_added(event)
        elif isinstance(event, CompetitionRemoved):
            self._handle_removed(event)
        elif isinstance(event, CompetitionNameChanged):
            self._handle_name_changed(event)
        elif isinstance(event, CompetitionDescriptionChanged):
            self._handle_description_changed(event)
        elif isinstance(event, CandidateAdded):
            self._handle_candidate_added(event)
        elif isinstance(event, CandidateRemoved):
            self._handle_candidate_removed(event)
        elif isinstance(event, CandidateNameChanged):
            self._handle_candidate_name_changed(event)
        elif isinstance(event, CandidateDescriptionChanged):
            self._handle_candidate_description_changed(event)
        elif isinstance(event, CandidateImageChanged):
            self._handle_candidate_image_changed(event)
        else:
            raise TypeError(f"Unexpected event type {type(event)} received by Competition-{self.id}")

    def ensure_valid_state(self):
        if not isinstance(self.id, CompetitionId):
            raise ValueError("Competition id must be of type CompetitionId")
        if self.id == AggregateId.empty():
            raise ValueError("Competition id must not be an empty ULID")
        if self.name == "":
            raise ValueError("Competition name cannot be empty")
        if self.description == "":
            raise ValueError("Competition description cannot be empty (use None instead)")

    def _handle_added(self, added: CompetitionAdded):
        self.id = CompetitionId(added.competition_id)
        self.name = CompetitionName(added.name)
        self.description = CompetitionDescription(added.description) if added.description else None

    def _handle_removed(self, removed: CompetitionRemoved):
        self.deleted = True

    def _handle_name_changed(self, changed: CompetitionNameChanged):
        self.name = CompetitionName(changed.name)

    def _handle_description_changed(self, changed: CompetitionDescriptionChanged):
        self.description = CompetitionDescription(changed.description) if changed.description else None

    def _handle_candidate_added(self, added: CandidateAdded):
        candidate_id = CandidateId(added.candidate_id)
        candidate = Candidate(candidate_id)
        candidate.name = CandidateName(added.name)
        candidate.description = CandidateDescription(added.description) if added.description else None
        self.candidates.append(candidate)

    def _handle_candidate_name_changed(self, changed: CandidateNameChanged):
        for candidate in self.candidates:
            if candidate.id == changed.candidate_id:
                candidate.name = CandidateName(changed.name)
                break

    def _handle_candidate_description_changed(self, changed: CandidateDescriptionChanged):
        for candidate in self.candidates:
            if candidate.id == changed.candidate_id:
                candidate.description = CandidateDescription(changed.description) if changed.description else None
                break

    def _handle_candidate_image_changed(self, changed: CandidateImageChanged):
        if changed.url is None and changed.caption is not None:
            raise ValueError("Candidate image URL must be set to set caption")
        for candidate in self.candidates:
            if candidate.id == changed.candidate_id:
                image_caption = ImageCaption(changed.caption) if changed.caption else None
                if changed.url:
                    image_url = ImageUrl(changed.url)
                    candidate.image = CandidateImage(url=image_url, caption=image_caption) if changed.url else None
                else:
                    candidate.image = None
                break

    def _handle_candidate_removed(self, removed: CandidateRemoved):
        for candidate in self.candidates:
            if candidate.id == removed.candidate_id:
                self.candidates.remove(candidate)
                break
