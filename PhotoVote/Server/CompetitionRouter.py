from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from memphis.producer import Producer, Headers

from PhotoVote.Event import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, CompetitionDescriptionChanged


class CompetitionRouter(APIRouter):
    def __init__(self, producer: Producer) -> None:
        super().__init__()
        self._memphis: Producer = producer

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
                                    headers=CompetitionRouter.headers(event_namespace, type(event).__name__))
        return Response(status_code=200)

    async def added(self, event: CompetitionAdded) -> Response:
        return await self._handle_event(event)

    async def removed(self, event: CompetitionRemoved) -> Response:
        return await self._handle_event(event)

    async def name(self, event: CompetitionNameChanged) -> Response:
        return await self._handle_event(event)

    async def description(self, event: CompetitionDescriptionChanged) -> Response:
        return await self._handle_event(event)
