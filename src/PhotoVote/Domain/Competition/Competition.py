from typing import Optional, List, Callable, Type, Dict

from pydantic import Field

from PhotoVote.Domain import Aggregate, AggregateId
from PhotoVote.Domain.Candidate import Candidate, CandidateName, CandidateDescription, CandidateImage, ImageUrl, \
    ImageCaption, CandidateId
from PhotoVote.Domain.Competition import CompetitionId, CompetitionName, CompetitionDescription
from PhotoVote.Event import Event
from PhotoVote.Event.Candidate import CandidateAdded, CandidateNameChanged, CandidateDescriptionChanged, \
    CandidateImageChanged, CandidateRemoved
from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged


class Competition(Aggregate[CompetitionId]):
    name: CompetitionName = CompetitionName("")
    description: Optional[CompetitionDescription] = None
    candidates: List[Candidate] = Field(default_factory=lambda: [])
    _handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._handlers = {
            CompetitionAdded: lambda e: self._handle_added(e),
            CompetitionRemoved: lambda e: self._handle_removed(e),
            CompetitionNameChanged: lambda e: self._handle_name_changed(e),
            CompetitionDescriptionChanged: lambda e: self._handle_description_changed(e),
            CandidateAdded: lambda e: self._handle_candidate_added(e),
            CandidateRemoved: lambda e: self._handle_candidate_removed(e),
            CandidateNameChanged: lambda e: self._handle_candidate_name_changed(e),
            CandidateDescriptionChanged: lambda e: self._handle_candidate_description_changed(e),
            CandidateImageChanged: lambda e: self._handle_candidate_image_changed(e)
        }

    def when(self, event: Event) -> None:
        if isinstance(event, tuple(self._handlers.keys())):
            self._handlers[type(event)](event)
        else:
            raise TypeError(f"Unexpected event type {type(event)} received by Competition-{self.id}")

    def ensure_valid_state(self) -> None:
        if not isinstance(self.id, CompetitionId):
            raise ValueError("Competition id must be of type CompetitionId")
        if self.id == AggregateId.empty():
            raise ValueError("Competition id must not be an empty ULID")
        if self.name == "":
            raise ValueError("Competition name cannot be empty")
        if self.description == "":
            raise ValueError("Competition description cannot be empty (use None instead)")

    def _handle_added(self, added: CompetitionAdded) -> None:
        self.id = CompetitionId(added.competition_id)
        self.name = CompetitionName(added.name)
        self.description = CompetitionDescription(added.description) if added.description else None

    def _handle_removed(self, removed: CompetitionRemoved) -> None:
        self.deleted = True

    def _handle_name_changed(self, changed: CompetitionNameChanged) -> None:
        self.name = CompetitionName(changed.name)

    def _handle_description_changed(self, changed: CompetitionDescriptionChanged) -> None:
        self.description = CompetitionDescription(changed.description) if changed.description else None

    def _handle_candidate_added(self, added: CandidateAdded) -> None:
        candidate_id = CandidateId(added.candidate_id)
        candidate = Candidate(id=candidate_id)
        candidate.name = CandidateName(added.name)
        candidate.description = CandidateDescription(added.description) if added.description else None
        self.candidates.append(candidate)

    def _handle_candidate_name_changed(self, changed: CandidateNameChanged) -> None:
        for candidate in self.candidates:
            if candidate.id == changed.candidate_id:
                candidate.name = CandidateName(changed.name)
                break

    def _handle_candidate_description_changed(self, changed: CandidateDescriptionChanged) -> None:
        for candidate in self.candidates:
            if candidate.id == changed.candidate_id:
                candidate.description = CandidateDescription(changed.description) if changed.description else None
                break

    def _handle_candidate_image_changed(self, changed: CandidateImageChanged) -> None:
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

    def _handle_candidate_removed(self, removed: CandidateRemoved) -> None:
        for candidate in self.candidates:
            if candidate.id == removed.candidate_id:
                self.candidates.remove(candidate)
                break
