import json

from server.SocketManager import SocketManager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers.ballot import router as ballot_router
from server.routers.candidate import router as candidate_router
from server.routers.competition import router as competition_router
from server.routers.election import router as election_router
from server.routers.security import router as security_router
from server.routers.voter import router as voter_router
from dotenv import load_dotenv

router = FastAPI()
router.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
sio = SocketManager(["http://localhost:3000", "http://localhost:8000"])

load_dotenv(".env")
router.include_router(security_router, prefix="/security")
router.include_router(ballot_router, prefix="/ballot")
router.include_router(candidate_router, prefix="/candidate")
router.include_router(competition_router, prefix="/competition")
router.include_router(election_router, prefix="/election")
router.include_router(voter_router, prefix="/voter")
router.mount("/", sio.app)


@sio.on("connect")
async def websocket_connect(sid, environ):
    print(f"WebSocket connected: {sid}")


@sio.on("disconnect")
async def websocket_disconnect(sid):
    print(f"WebSocket disconnected: {sid}")


@sio.on("connect_error")
async def websocket_error(sid, error):
    print(f"WebSocket connection failed: {error}")


@sio.on("response")
async def push_response(sid, message):
    response = json.loads(message)
    await sio.emit("response", to=response["recipient"], data=message)
