from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from memphis.producer import Producer, Headers

from PhotoVote.Event import VoterRegistered


class VoterRouter(APIRouter):
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

    async def _handle_event(self, event, event_namespace: str = "PhotoVote.Event",
                            package_reference: str = "PhotoVote.Event") -> Response:
        await self._memphis.produce(event.model_dump_json(),
                                    headers=VoterRouter.headers(event_namespace, type(event).__name__, package_reference))
        return Response(status_code=200)

    # Voter is a read-only aggregate that can be added to any election. It is immutable after creation and cannot be
    # deleted, so this is the only method in this router.
    async def registered(self, event: VoterRegistered):
        await self._handle_event(event)
