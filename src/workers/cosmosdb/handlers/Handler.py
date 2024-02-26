from typing import Optional

from azure.cosmos.aio import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from PhotoVote.Domain.Election import Election, ElectionId
from PhotoVote.Event import Event


class Handler:
    _container: ContainerProxy

    def __init__(self, container: ContainerProxy):
        self._container = container

    async def _get(self, election_id: str) -> Optional[Election]:
        try:
            election_dict = await self._container.read_item(election_id, election_id)
            election = Election.model_validate(election_dict)
            return election
        except CosmosResourceNotFoundError:
            return None

    async def _upsert(self, election: Election) -> None:
        election_dict = election.model_dump()
        await self._container.upsert_item(election_dict)

    async def _delete(self, election_id) -> None:
        await self._container.delete_item(election_id, election_id)

    async def handle(self, event: Event):
        election = await self._get(event.election_id)
        if election is None:
            election = Election(id=ElectionId(event.election_id))
        election.apply(event)
        if not election.deleted:
            await self._upsert(election)
        else:
            await self._delete(election.id)
