from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from memphis import Headers
from memphis.producer import Producer

from PhotoVote.Event import Event
from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged
from server.ApiUser import ApiUser
from server.dependencies import get_election_producer, get_current_user

router = APIRouter()


async def _produce_message(message: Event, producer: Producer, user: ApiUser):
    headers = Headers()
    headers.add("Request-Type", message.__module__)
    headers.add("User", user.email)
    await producer.produce(message=message.model_dump_json().encode("utf-8"), headers=headers)


@router.post("/")
async def competition_added(added: CompetitionAdded,
                            producer: Producer = Depends(get_election_producer),
                            user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(added, producer, user)
    return JSONResponse(status_code=200, content={})


@router.delete("/")
async def competition_removed(removed: CompetitionRemoved,
                              producer: Producer = Depends(get_election_producer),
                              user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(removed, producer, user)
    return JSONResponse(status_code=200, content={})


@router.put("/name-changed")
async def competition_name_changed(changed: CompetitionNameChanged,
                                   producer: Producer = Depends(get_election_producer),
                                   user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(changed, producer, user)
    return JSONResponse(status_code=200, content={})


@router.put("/description-changed")
async def competition_description_changed(changed: CompetitionDescriptionChanged,
                                          producer: Producer = Depends(get_election_producer),
                                          user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(changed, producer, user)
    return JSONResponse(status_code=200, content={})
