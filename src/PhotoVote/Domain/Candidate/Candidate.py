from typing import Optional

from PhotoVote.Domain import AggregateRoot, AggregateId
from PhotoVote.Domain.Candidate import CandidateId, CandidateName, CandidateDescription, CandidateImage
from PhotoVote.Event import Event
from PhotoVote.Event.Candidate import CandidateAdded, CandidateRemoved, CandidateNameChanged, \
    CandidateDescriptionChanged, CandidateImageChanged


class Candidate(AggregateRoot[CandidateId]):
    name: CandidateName = CandidateName("")
    description: Optional[CandidateDescription] = None
    image: Optional[CandidateImage] = None

    def __init__(self, candidate_id: CandidateId):
        super().__init__(candidate_id)

    def when(self, event: Event):
        if isinstance(event, CandidateAdded):
            self._handle_added(event)
        elif isinstance(event, CandidateRemoved):
            self._handle_removed(event)
        elif isinstance(event, CandidateNameChanged):
            self._handle_name_changed(event)
        elif isinstance(event, CandidateDescriptionChanged):
            self._handle_description_changed(event)
        elif isinstance(event, CandidateImageChanged):
            self._handle_image_changed(event)
        else:
            raise ValueError(f"Unknown event type {event.__class__.__name__} received by Candidate aggregate")

    def ensure_valid_state(self):
        if not isinstance(self.id, CandidateId):
            raise ValueError("Candidate aggregate must have an id of type CandidateId")
        if self.id == AggregateId.empty():
            raise ValueError("Candidate id cannot be empty")
        if self.name == "":
            raise ValueError("Candidate name cannot be empty")
        if self.description == "":
            raise ValueError("Candidate description cannot be empty (use None instead)")

    def _handle_added(self, added: CandidateAdded):
        self.id = CandidateId(added.candidate_id)
        self.name = CandidateName(added.name)
        self.description = CandidateDescription(added.description) if added.description is not None else None
        if added.image_url is None and added.image_caption is not None:
            raise ValueError("Candidate image URL must be set to provide caption")
        self.image = CandidateImage(added.image_url, added.image_caption) if added.image_url is not None else None

    def _handle_removed(self, removed: CandidateRemoved):
        self.delete()

    def _handle_name_changed(self, changed: CandidateNameChanged):
        self.name = CandidateName(changed.name)

    def _handle_description_changed(self, changed: CandidateDescriptionChanged):
        self.description = CandidateDescription(changed.description) if changed.description is not None else None

    def _handle_image_changed(self, changed: CandidateImageChanged):
        if changed.url is None and changed.caption is not None:
            raise ValueError("Image URL must be set to set caption")
        self.image = CandidateImage(changed.url,
                                    changed.caption) if changed.url is not None else None
