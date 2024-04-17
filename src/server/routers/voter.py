from fastapi import APIRouter
from fastapi.responses import JSONResponse
from memphis import Headers
from memphis.producer import Producer

from PhotoVote.Event import Event
from PhotoVote.Event.Voter import VoterRegistered
from server.ApiUser import ApiUser

router = APIRouter()


async def _produce_message(message: Event, producer: Producer, user: ApiUser):
    headers = Headers()
    headers.add("Request-Type", message.__module__)
    headers.add("User", user.email)
    await producer.produce(message=message.model_dump_json().encode("utf-8"), headers=headers)


@router.post("/")
async def voter_registered(registered: VoterRegistered):
    return JSONResponse(status_code=200, content={})
