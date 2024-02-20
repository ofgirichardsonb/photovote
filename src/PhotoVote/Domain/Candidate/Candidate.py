from typing import Optional, Callable, Type, Dict

from PhotoVote.Domain import Aggregate, AggregateId
from PhotoVote.Domain.Candidate import CandidateId, CandidateName, CandidateDescription, CandidateImage, ImageUrl, \
    ImageCaption
from PhotoVote.Event import Event
from PhotoVote.Event.Candidate import CandidateAdded, CandidateRemoved, CandidateNameChanged, \
    CandidateDescriptionChanged, CandidateImageChanged


class Candidate(Aggregate[CandidateId]):
    name: CandidateName = CandidateName("")
    description: Optional[CandidateDescription] = None
    image: Optional[CandidateImage] = None
    _handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, candidate_id: CandidateId):
        super().__init__(candidate_id)
        self._handlers = {
            CandidateAdded: lambda e: self._handled_added(e),
            CandidateRemoved: lambda e: self._handled_removed(e),
            CandidateNameChanged: lambda e: self._handle_name_changed(e),
            CandidateDescriptionChanged: lambda e: self._handle_description_changed(e),
            CandidateImageChanged: lambda e: self._handle_image_changed(e)
        }

    def when(self, event: Event) -> None:
        if isinstance(event, tuple(self._handlers.keys())):
            self._handlers[type(event)](event)
        else:
            raise ValueError(f"Unknown event type {event.__class__.__name__} received by Candidate aggregate")

    def ensure_valid_state(self) -> None:
        if not isinstance(self.id, CandidateId):
            raise ValueError("Candidate aggregate must have an id of type CandidateId")
        if self.id == AggregateId.empty():
            raise ValueError("Candidate id cannot be empty")
        if self.name == "":
            raise ValueError("Candidate name cannot be empty")
        if self.description == "":
            raise ValueError("Candidate description cannot be empty (use None instead)")

    def _handle_added(self, added: CandidateAdded) -> None:
        self.id = CandidateId(added.candidate_id)
        self.name = CandidateName(added.name)
        self.description = CandidateDescription(added.description) if added.description is not None else None
        if added.image_url is None and added.image_caption is not None:
            raise ValueError("Candidate image URL must be set to provide caption")
        image_caption = ImageCaption(added.image_caption) if added.image_caption else None
        if added.image_url is not None:
            image_url = ImageUrl(added.image_url)
            self.image = CandidateImage(url=image_url, caption=image_caption)
        else:
            self.image = None

    def _handle_removed(self, removed: CandidateRemoved) -> None:
        self.delete()

    def _handle_name_changed(self, changed: CandidateNameChanged) -> None:
        self.name = CandidateName(changed.name)

    def _handle_description_changed(self, changed: CandidateDescriptionChanged) -> None:
        self.description = CandidateDescription(changed.description) if changed.description is not None else None

    def _handle_image_changed(self, changed: CandidateImageChanged) -> None:
        if changed.url is None and changed.caption is not None:
            raise ValueError("Image URL must be set to set caption")
        image_caption = ImageCaption(changed.caption) if changed.caption else None
        if changed.url is not None:
            image_url = ImageUrl(changed.url)
            self.image = CandidateImage(url=image_url, caption=image_caption)
        else:
            self.image = None
