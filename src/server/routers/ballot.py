from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from memphis import Headers
from memphis.producer import Producer

from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from ..ApiUser import ApiUser
from ..dependencies import get_election_producer, get_current_user

router = APIRouter()


async def _produce_message(message: Event, producer: Producer, user: ApiUser):
    headers = Headers()
    headers.add("Request-Type", message.__module__)
    headers.add("User", user.email)
    await producer.produce(message=message.model_dump_json().encode("utf-8"), headers=headers)


@router.post("/")
async def ballot_created(created: BallotCreated,
                         producer: Producer = Depends(get_election_producer),
                         user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(created, producer, user)
    return JSONResponse(status_code=200, content={})


@router.put("/candidate-rated")
async def candidate_rated(rated: BallotCandidateRated,
                          producer: Producer = Depends(get_election_producer),
                          user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(rated, producer, user)
    return JSONResponse(status_code=200, content={})


@router.post(path="/cast")
async def ballot_cast(cast: BallotCast,
                      producer: Producer = Depends(get_election_producer),
                      user: ApiUser = Depends(get_current_user)) -> JSONResponse:
    await _produce_message(cast, producer, user)
    return JSONResponse(status_code=200, content={})
