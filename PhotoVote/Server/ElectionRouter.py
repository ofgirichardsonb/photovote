from typing import Optional
from memphis import Headers
from memphis.producer import Producer

from fastapi import Response, APIRouter

from PhotoVote.Event import ElectionCreated, ElectionDeleted, ElectionNameChanged, ElectionDescriptionChanged


class ElectionRouter(APIRouter):
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
                                    headers=ElectionRouter.headers(event_namespace, type(event).__name__))
        return Response(status_code=200)

    async def created(self, event: ElectionCreated):
        return await self._handle_event(event)

    async def deleted(self, event: ElectionDeleted):
        return await self._handle_event(event)

    async def name(self, event: ElectionNameChanged):
        return await self._handle_event(event)

    async def description(self, event: ElectionDescriptionChanged):
        return await self._handle_event(event)
