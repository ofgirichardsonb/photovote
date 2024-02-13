from fastapi import APIRouter
from fastapi.responses import JSONResponse

from PhotoVote.Event.Candidate import CandidateAdded, CandidateNameChanged, CandidateDescriptionChanged, \
    CandidateImageChanged
from .Router import Router

router = APIRouter()
candidate_router = Router("candidate", ["election"])


@router.post("/")
async def candidate_added(created: CandidateAdded) -> JSONResponse:
    await candidate_router.publish_event(created)
    return JSONResponse(status_code=200, content={})


@router.delete("/")
async def candidate_removed(removed: CandidateNameChanged) -> JSONResponse:
    await candidate_router.publish_event(removed)
    return JSONResponse(status_code=200, content={})


@router.put("/name-changed")
async def candidate_name_changed(changed: CandidateNameChanged) -> JSONResponse:
    await candidate_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})


@router.put("/description-changed")
async def candidate_description_changed(changed: CandidateDescriptionChanged) -> JSONResponse:
    await candidate_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})


@router.put("/image-changed")
async def candidate_image_changed(changed: CandidateImageChanged) -> JSONResponse:
    await candidate_router.publish_event(changed)
    return JSONResponse(status_code=200, content={})
