from fastapi import APIRouter
from fastapi.responses import JSONResponse

from PhotoVote.Event.Voter import VoterRegistered
from .Router import Router

router = APIRouter()
voter_router = Router("voter", ["election"])


@router.post("/")
async def voter_registered(registered: VoterRegistered):
    await voter_router.publish_event(registered)
    return JSONResponse(status_code=200, content={})
