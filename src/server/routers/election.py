import json

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from memphis import Headers
from memphis.producer import Producer

from PhotoVote.Event import Event
from PhotoVote.Event.Election import ElectionCreated, ElectionDeleted, ElectionNameChanged, \
    ElectionDescriptionChanged, ElectionOpened, ElectionClosed
from ..dependencies import get_current_user, get_election_producer
from ..ApiUser import ApiUser


router = APIRouter()


async def _produce_message(message: Event, producer: Producer, user: ApiUser):
    headers = Headers()
    headers.add("Request-Type", message.__module__)
    headers.add("User", user.email)
    await producer.produce(message=message.model_dump_json().encode("utf-8"), headers=headers)


@router.post("/")
async def election_created(created: ElectionCreated,
                           producer: Producer = Depends(get_election_producer),
                           user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(created, producer, user)
    return JSONResponse(status_code=200, content={})
    
    
@router.delete("/")
async def election_deleted(removed: ElectionDeleted,
                           producer: Producer = Depends(get_election_producer),
                           user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(removed, producer, user)
    return JSONResponse(status_code=200, content={})


@router.put("/name-changed")
async def election_name_changed(changed: ElectionNameChanged,
                                producer: Producer = Depends(get_election_producer),
                                user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(changed, producer, user)
    return JSONResponse(status_code=200, content={})
    

@router.put("/description-changed")
async def election_description_changed(changed: ElectionDescriptionChanged,
                                       producer: Producer = Depends(get_election_producer),
                                       user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(changed, producer, user)
    return JSONResponse(status_code=200, content={})


@router.put("/opened")
async def election_opened(opened: ElectionOpened,
                          producer: Producer = Depends(get_election_producer),
                          user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(opened, producer, user)
    return JSONResponse(status_code=200, content={})
    

@router.put("/closed")
async def election_closed(closed: ElectionClosed,
                          producer: Producer = Depends(get_election_producer),
                          user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(closed, producer, user)
    return JSONResponse(status_code=200, content={})
