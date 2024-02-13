from fastapi import APIRouter
from fastapi.responses import JSONResponse
from PhotoVote.Event.Election import ElectionCreated, ElectionDeleted, ElectionNameChanged, \
    ElectionDescriptionChanged, ElectionOpened, ElectionClosed
    
from .Router import Router


router = APIRouter()
election_router = Router("election", ["election"])


@router.post("/")
async def election_created(created: ElectionCreated) -> JSONResponse:
    await election_router.publish_event(created)
    return JSONResponse(status_code=200, content={})
    
    
@router.delete("/")
async def election_deleted(removed: ElectionDeleted) -> JSONResponse:
    await election_router.publish_event(removed)
    return JSONResponse(status_code=200, content={})


@router.put("/name-changed")
async def election_name_changed(changed: ElectionNameChanged) -> JSONResponse:
    await election_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})
    

@router.put("/description-changed")
async def election_description_changed(changed: ElectionDescriptionChanged) -> JSONResponse:
    await election_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})


@router.put("/opened")
async def election_opened(opened: ElectionOpened) -> JSONResponse:
    await election_router.publish_event(opened)
    return JSONResponse(status_code=200, content={})
    

@router.put("/closed")
async def election_closed(closed: ElectionClosed) -> JSONResponse:
    await election_router.publish_event(closed)
    return JSONResponse(status_code=200, content={})
