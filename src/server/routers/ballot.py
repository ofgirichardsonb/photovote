from fastapi import APIRouter
from fastapi.responses import JSONResponse

from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from .Router import Router

router = APIRouter()
ballot_router: Router = Router("ballot", ["election"])


@router.post("/")
async def ballot_created(created: BallotCreated) -> JSONResponse:
    await ballot_router.publish_event(created)
    return JSONResponse(status_code=200, content={})


@router.put("/candidate-rated")
async def candidate_rated(rated: BallotCandidateRated) -> JSONResponse:
    await ballot_router.publish_event(rated)
    return JSONResponse(status_code=200, content={})


@router.post(path="/cast")
async def ballot_cast(cast: BallotCast) -> JSONResponse:
    await ballot_router.publish_event(cast)
    return JSONResponse(status_code=200, content={})
