from fastapi import APIRouter
from fastapi.responses import JSONResponse

from PhotoVote.Event.Competition import CompetitionAdded, CompetitionRemoved, CompetitionNameChanged, \
    CompetitionDescriptionChanged
from server.routers.Router import Router

router = APIRouter()
competition_router = Router("competition", ["election"])


@router.post("/")
async def competition_added(added: CompetitionAdded) -> JSONResponse:
    await competition_router.publish_event(added)
    return JSONResponse(status_code=200, content={})


@router.delete("/")
async def competition_removed(removed: CompetitionRemoved) -> JSONResponse:
    await competition_router.publish_event(removed)
    return JSONResponse(status_code=200, content={})


@router.put("/name-changed")
async def competition_name_changed(changed: CompetitionNameChanged) -> JSONResponse:
    await competition_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})


@router.put("/description-changed")
async def competition_description_changed(changed: CompetitionDescriptionChanged) -> JSONResponse:
    await competition_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})
