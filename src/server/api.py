from fastapi import FastAPI
from server.routers.ballot import router as ballot_router
from server.routers.candidate import router as candidate_router
from server.routers.competition import router as competition_router
from server.routers.election import router as election_router
from server.routers.voter import router as voter_router
from dotenv import load_dotenv

router = FastAPI()

load_dotenv(".env")
router.include_router(ballot_router, prefix="/ballot")
router.include_router(candidate_router, prefix="/candidate")
router.include_router(competition_router, prefix="/competition")
router.include_router(election_router, prefix="/election")
router.include_router(voter_router, prefix="/voter")
