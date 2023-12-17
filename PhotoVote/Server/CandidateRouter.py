from typing import Optional
from fastapi import APIRouter, Response
from memphis import Headers
from memphis.producer import Producer

from PhotoVote.Event import CandidateAdded, CandidateRemoved, CandidateNameChanged, CandidateDescriptionChanged, \
    CandidateImageUrlChanged, CandidateImageCaptionChanged


class CandidateRouter(APIRouter):
    def __init__(self, memphis: Producer):
        super().__init__()
        self._memphis: Producer = memphis

    @staticmethod
    def headers(event_namespace: str, event_type: str, package_reference: Optional[str] = None):
        headers = Headers()
        headers.add("EventNamespace", event_namespace)
        headers.add("EventType", event_type)
        # PackageReference is only necessary if it differs from EventNamespace, which it is not
        # in a project with no subpackages of the main event package
        headers.add("PackageReference", package_reference) if package_reference else None
        return headers

    async def _handle_event(self, event, event_namespace: str = "PhotoVote.Event") -> Response:
        await self._memphis.produce(event.model_dump_json(),
                                    headers=CandidateRouter.headers(event_namespace, type(event).__name__))
        return Response(status_code=200)

    async def added(self, event: CandidateAdded) -> Response:
        return await self._handle_event(event)

    async def removed(self, event: CandidateRemoved) -> Response:
        return await self._handle_event(event)

    async def name(self, event: CandidateNameChanged) -> Response:
        return await self._handle_event(event)

    async def description(self, event: CandidateDescriptionChanged) -> Response:
        return await self._handle_event(event)

    async def imageurl(self, event: CandidateImageUrlChanged) -> Response:
        return await self._handle_event(event)

    async def imagecaption(self, event: CandidateImageCaptionChanged) -> Response:
        return await self._handle_event(event)