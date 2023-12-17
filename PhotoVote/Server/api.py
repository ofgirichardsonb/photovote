from typing import List, Callable, Awaitable
from fastapi import FastAPI
from fastapi.responses import Response
from memphis import Memphis
from memphis.producer import Producer
import asyncio
from PhotoVote.Event import BallotCast, BallotCandidateRated, CandidateAdded, CandidateRemoved, CandidateNameChanged, \
    CandidateDescriptionChanged, CandidateImageUrlChanged, CandidateImageCaptionChanged, CompetitionAdded, \
    CompetitionRemoved, CompetitionNameChanged, CompetitionDescriptionChanged, ElectionCreated, ElectionDeleted, \
    ElectionNameChanged, ElectionDescriptionChanged, VoterRegistered
from PhotoVote.Server.BallotRouter import BallotRouter
from PhotoVote.Server.CandidateRouter import CandidateRouter
from PhotoVote.Server.CompetitionRouter import CompetitionRouter
from PhotoVote.Server.ElectionRouter import ElectionRouter
from PhotoVote.Server.VoterRouter import VoterRouter
from dotenv import load_dotenv
import os

app = FastAPI()
memphis = Memphis()
load_dotenv()

MEMPHIS_HOST: str = os.getenv("MEMPHIS_HOST")
MEMPHIS_USERNAME: str = os.getenv("MEMPHIS_USERNAME")
MEMPHIS_ACCOUNT_ID: int = int(os.getenv("MEMPHIS_ACCOUNT_ID"))
MEMPHIS_PASSWORD: str = os.getenv("MEMPHIS_PASSWORD")


async def get_producer(station_name: str | List[str], producer_name: str) -> Producer:
    await memphis.connect(MEMPHIS_HOST, MEMPHIS_USERNAME, MEMPHIS_ACCOUNT_ID, password=MEMPHIS_PASSWORD)
    return await memphis.producer(station_name=station_name, producer_name=producer_name)


@app.on_event("startup")
def startup_event():
    asyncio.create_task(main())


async def setup_ballot_routes(producer: Producer) -> None:
    ballot_router = BallotRouter(producer)

    @ballot_router.post("/cast")
    async def cast_ballot(event: BallotCast) -> Response:
        return await ballot_router.cast(event)

    @ballot_router.put("/candidaterated")
    async def rate_candidate(event: BallotCandidateRated) -> Response:
        return await ballot_router.candidate_rated(event)

    app.include_router(ballot_router, prefix="/ballot")


async def setup_candidate_routes(producer: Producer) -> None:
    candidate_router = CandidateRouter(producer)

    @candidate_router.post("/")
    async def added(event: CandidateAdded) -> Response:
        return await candidate_router.added(event)

    @candidate_router.delete("/")
    async def removed(event: CandidateRemoved) -> Response:
        return await candidate_router.removed(event)

    @candidate_router.put("/name")
    async def name(event: CandidateNameChanged) -> Response:
        return await candidate_router.name(event)

    @candidate_router.put("/description")
    async def description(event: CandidateDescriptionChanged) -> Response:
        return await candidate_router.description(event)

    @candidate_router.put("/imageurl")
    async def imageurl(event: CandidateImageUrlChanged) -> Response:
        return await candidate_router.imageurl(event)

    @candidate_router.put("/imagecaption")
    async def imagecaption(event: CandidateImageCaptionChanged) -> Response:
        return await candidate_router.imagecaption(event)

    app.include_router(candidate_router, prefix="/candidate")


async def setup_competition_routes(producer: Producer) -> None:
    competition_router = CompetitionRouter(producer)

    @competition_router.post("/")
    async def added(event: CompetitionAdded) -> Response:
        return await competition_router.added(event)

    @competition_router.delete("/")
    async def removed(event: CompetitionRemoved) -> Response:
        return await competition_router.removed(event)

    @competition_router.put("name")
    async def name_changed(event: CompetitionNameChanged) -> Response:
        return await competition_router.name(event)

    @competition_router.put("description")
    async def description_changed(event: CompetitionDescriptionChanged) -> Response:
        return await competition_router.description(event)

    app.include_router(competition_router, prefix="/competition")


async def setup_election_routes(producer: Producer) -> None:
    election_router = ElectionRouter(producer)

    @election_router.post("/")
    async def create(event: ElectionCreated) -> Response:
        return await election_router.created(event)

    @election_router.delete("/")
    async def delete(event: ElectionDeleted) -> Response:
        return await election_router.deleted(event)

    @election_router.put("/name")
    async def name(event: ElectionNameChanged) -> Response:
        return await election_router.name(event)

    @election_router.put("/description")
    async def description(event: ElectionDescriptionChanged) -> Response:
        return await election_router.description(event)

    app.include_router(election_router, prefix="/election")


async def setup_voter_routes(producer: Producer) -> None:
    voter_router = VoterRouter(producer)

    @voter_router.post("/")
    async def registered(event: VoterRegistered) -> Response:
        return await voter_router.registered(event)

    app.include_router(voter_router, prefix="/voter")


async def setup(stations: List[str], producer_name: str, setup_routes: Callable[[Producer], Awaitable[None]]):
    producer = await get_producer(stations, producer_name)
    await setup_routes(producer)


async def main():
    try:
        tasks = [
            setup(["election", "ballot"], "BallotProducer", setup_ballot_routes),
            setup(["election", "candidate", "competition"], "CandidateProducer", setup_candidate_routes),
            setup(["election", "competition"], "CompetitionProducer", setup_competition_routes),
            setup(["election"], "ElectionProducer", setup_election_routes),
            setup(["election", "voter"], "VoterProducer", setup_voter_routes)
        ]
        await asyncio.gather(*tasks)
    except Exception as e:
        await memphis.close()
