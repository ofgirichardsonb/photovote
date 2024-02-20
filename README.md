
# PhotoVote

## A Demonstration of Event Sourcing and DDD with Python

This is a port of a C# event-sourced application.
Translating to Python is an interesting exercise, because there are
many philosophical differences between the languages that result in
very different code in Python.
While not as formal or strict, the essence of Event Sourcing is
definitely there. 
Additionally, this program demonstrates the use of DDD techniques.
The use of Pydantic greatly eases the Python implementation, and I
really like Python's native JSON support here.

## Overview of the Application

The application itself is relatively simple, a multi-user application
that allows users to vote on photographs posted by an administrator.
When the election is closed, the administrator can then view the
results.

The application has three parts:
* The FastAPI API
* An EventStore worker, for storing incoming events into EventStoreDB
* A CosmosDB worker, to subscribe to events in EventStore and
  make corresponding updates in CosmosDB.

Let's look at each in turn.

## API

### DDD

It's relatively easy to identify the aggregates in this application.
The aggregates are analogous to entities in an ORM-based system.
We also need to identify the aggregate root for the application
domain (and there really is only one domain. More complex 
applications will have multiple domains and aggregate roots). 
In this case, we can easily identify the following aggregate types:
* **Election** - the aggregate root; all other aggregates are part
  of an `Election` object hierarchy.
* **Competition** - An `Election` is composed of one or more
  `Competition`s
* **Candidate** - A `Competition` will present two or more
  `Candidate`s
* **Voter** - `Election`s require `Voter`s. Each user will be a
  `Voter`.
* **Ballot** - Each `Voter` will receive exactly one `Ballot` for
  recording their ratings for each `Candidate`.

After identifying the aggregates, we also need to identify the
properties and create types for them. 
For example:

```python
from typing import Optional

from PhotoVote.Domain import Aggregate
from PhotoVote.Domain.Election import ElectionName, ElectionDescription


class Election(Aggregate):
    name: ElectionName
    description: Optional[ElectionDescription] = None

# ...
```

DDD style is recognizable by its very strong typing.
As you can see in the `Election` class, `name` and `description` are
not strings, rather they are types that wrap strings. 
Let's look at one really quickly:

```python
from pydantic import RootModel

class ElectionName(RootModel):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return self.root
```

As you can see, it's just a really thin wrapper over a string.
So why do we do this?
In addition to being more readable, it also makes it clear what
*type* of `str` something is.
Is an `ElectionName` equal to an `ElectionDescription` just because
they contain the same text?
Is an `ElectionId` equal to a `CompetitionId` just because they
contain the same value?
In DDD, the answer is "no". 
The addition of type information is a bit of extra effort, but it
can prevent you from making subtle mistakes that are hard to find.

### Event Sourcing

Many designs will stop with DDD and use traditional application
architectures like MVC backed by traditional SQL databases.
However, Event Sourcing takes things another step, and makes the
domain objects more robust by restricting the changes that can
be made to a domain object.
Every change to a domain object must be accompanied by an event.
In fact, the domain object can only be modified by applying an
event; it is forbidden (at least by convention) to modify the
individual properties outside the context of the event handler.
Let's look at the definition of `Aggregate` to see how that is
accomplished:

```python
from abc import abstractmethod
from typing import Generic, TypeVar, List

from pydantic import BaseModel

from PhotoVote.Event import Event
from PhotoVote.Exception import AlreadyDeletedError

T = TypeVar('T')


class BaseAggregate(BaseModel):
    version: int = -1
    deleted: bool = False

    @abstractmethod
    def when(self, event: Event):
        pass

    @abstractmethod
    def ensure_valid_state(self):
        pass

    def apply(self, event):
        if self.deleted:
            raise AlreadyDeletedError()
        self.when(event)
        self.ensure_valid_state()
        self.version = self.version + 1

    def load(self, events: List[Event]):
        if self.deleted:
            raise AlreadyDeletedError()
        for event in events:
            self.when(event)
            self.version = self.version + 1
        self.ensure_valid_state()

    def delete(self):
        if self.deleted:
            raise AlreadyDeletedError()
        self.deleted = True


class Aggregate(BaseAggregate, Generic[T]):
    id: T

    def __init__(self, aggregate_id: T):
        super().__init__(id=aggregate_id)

    @abstractmethod
    def when(self, event: Event):
        pass

    @abstractmethod
    def ensure_valid_state(self):
        pass
```

There's a lot here, but it's really important, so let's spend some
time unpacking it.
First, note that the `BaseAggregate` is a Pydantic model.
This gives us the methods `model_dump_json()` and 
`model_validate_json()`. 
Incredibly, without any additional code, the `Aggregate` can be 
converted to and from JSON with very little effort.
Next, we see the abstract `when()` and `ensure_valid_state()` methods.
These methods are overriden by each aggregate type to modify the
aggregate state in response to an event, and to ensure that the
state of the resulting aggregate is valid. 
Let's look at a quick example of this:

```python
from typing import Dict, Type, Callable

from pydantic import Field

from PhotoVote.Domain import Aggregate, AggregateId
from PhotoVote.Domain.Ballot import BallotId, Rating
from PhotoVote.Domain.Candidate import CandidateId
from PhotoVote.Domain.Competition import CompetitionId
from PhotoVote.Event import Event
from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast


class Ballot(Aggregate[BallotId]):
    ratings: Dict[CompetitionId, Dict[CandidateId, Rating]] = Field(default_factory=lambda: {})
    cast: bool = False
    handlers: Dict[Type[Event], Callable[[Event], None]]

    def __init__(self, ballot_id: BallotId):
        super().__init__(ballot_id)
        self.handlers = {
            BallotCast: self._handle_ballot_cast,
            BallotCreated: self._handle_ballot_created,
            BallotCandidateRated: self._handle_candidate_rated
        }

    def when(self, event: Event):
        if isinstance(event, tuple(self.handlers.keys())):
            self.handlers[type(event)](event)
        else:
            raise ValueError(f"Unknown event type {event.__class__.__name__}")

    def ensure_valid_state(self):
        if not isinstance(self.id, BallotId):
            raise ValueError("Ballot id must be of type BallotId")
        if self.id == AggregateId.empty():
            raise ValueError("Ballot ID cannot be empty")
```
First, notice that we have created a `handlers` table in the
constructor.
This table will be consulted to determine which instance method
to call when an event is received, as seen in the `when()` method.
`apply()` calls `when()` and `ensure_valid_state()` in succession;
every event's result will be validated.

It is extremely important that this `when()` method be thorough
and handle every single event that is relevant to the aggregate,
even ones that are primarily associated with another aggregate.
For example, the `Election` aggregate represents the entire document.
It will be affected by every event in the application.
It is also extremely important that aggregates never get modified
outside the event handler, since those changes will not be stored
in EventStoreDB. 
EventStoreDB works by storing a stream of events; there is no
single document or table that stores data; rather it is
aggregated by reapplying all the events stored there (hence the
name "aggregate").
This means that while EventStoreDB is an authoritative source, it
is not really queryable except to get the current state of a single
entity.
In practice, this is never done.
The current state of the entity will be stored in CosmosDB for
convenience, and CosmosDB kept updated by subscribing to EventStore
and making incremental updates to CosmosDB as events arrive.

So why the extra layer? 
Wouldn't it be easier to simply message the CosmosDB worker directly?
Primarily, the purpose of doing so is for audit and resilience reasons.
By keeping a copy of every event in the system and who caused it, it is
possible for audit to obtain this information at a granularity we have not
not been capable of. 
Coupled with the immutability of EventStoreDB, this provides a reliable
source of information that can be replayed at any time to rebuild the
document cache. 
A single change can corrupt a database not backed by EventStore.
Without the EventStore to replay changes and rebuild the current
state, there is a lower confidence that the corruption has been addressed.
With the backing of EventStore, every single change can be examined in
isolation, remediated, and the database rebuilt.

Likewise, the `ensure_valid_state()` method must be fully implemented.
Removing buggy events from EventStore is not easy, as it is designed
to be immutable. 
While entire streams can be removed, individual events can
only be undone by creating and applying and remediating event. 
As this is not a good result, it's critical that this method be
as thorough as possible, and as much testing as possible be done.

## Conventions

This architecture is dependent on being organized and named in a
predictable way.

### Events

All event classes must extend `PhotoVote.Event.Event`.
This is itself a Pydantic `BaseModel`, so you can treat any `Event`
subclass as a Pydantic model.
The following conventions should be followed when creating an
`Event`:

1. `Event`s are made up of primitives; do not use the DDD types in
   the `Event`.
2. You should provide all id values in the hierarchy. 
   For example, when sending an `Event` for a `Candidate`, you should
   send the `election_id`, `competition_id`, and `candidate_id`.
3. The names of the id fields should be `<aggregate-name>_id`.
4. All fields (except `id`) in an `Event` must be `Optional` and 
   default to `None` as it is necessary to construct event instances
   from just their ids.
5. Events should have a namespace that corresponds to the type
   of aggregate it is primarily associated with. 
   While some events apply to more than one aggregate type, it 
   should be relatively obvious in most cases which one it is most
   associated with.
   Organizing in this fashion allows necessary imports to be
   located easily.
   For example, `BallotCandidateRated` is most associated with a
   `Ballot`, because the event directly affects a `Ballot`, and only
   indirectly affects the `Election` (since a `Ballot` instance is
   part of the `Election`).
   Therefore, it should be named `BallotCandidateRated` and
   placed in the `PhotoVote.Event.Ballot` namespace.

### Aggregates

All aggregate classes must extend `PhotoVote.Domain.Aggregate`. 
They should have an aggregate id type named `<Aggregate-Name>Id`.
The aggregate id type must extend `PhotoVote.Domain.AggregateId`.
`AggregateId`s are constructed from a ULID `str`. 
The aggregate should be the final picture of the document that
will be stored in the database. 
Its JSON representation is what will be stored in the document cache.

#### DDD Typing

Follow the example above for `ElectionName` for any primitive 
properties.
You should extend `RootModel` and accept a constructor parameter
of the desired primitive type. 
Remember to write casting operators such as `__str__` as well to
return the root value.
Complex values such as `Election` can also be declared as properties
provided they extend `Aggregate` or `RootModel`.
Doing so ensures that the JSON produced will be accurate, and that
it can be read back into the aggregate.

### A note on Pydantic

Pydantic models are being used here to facilitate the conversion of
aggregates and events to and from JSON. 
There's a lot of additional
code we don't see as a result (often a good thing, as long as you're
aware that is there and what it is doing).
That said, you should use native Python objects when you can (i.e.,
if you don't require a JSON representation or other Pydantic features).
This will reduce the memory requirements of the application and
slightly improve performance.

### Conclusion

If you adhere to the conventions, it becomes easy to write
the API, as all business logic is contained in the event
handlers within the domain model. 
We have an ideal state where all business rules are captured
within the domain model, and an invalid state cannot be committed
to the event store.
Here is the root `api.py` FastAPI application:

```python
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
```

The routers are not much more complicated:

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from PhotoVote.Event.Ballot import BallotCreated, BallotCandidateRated, BallotCast
from server.routers.Router import Router

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
```

The workhorse here is the `Router` class, which is also
quite straightforward:

```python
from typing import List, Optional

from memphis import Memphis, Headers
from memphis.producer import Producer
from uuid import uuid4

from PhotoVote.Event import Event
import os


class Router:
    _name: str
    _stations: List[str]
    _producer: Optional[Producer] = None

    def __init__(self, name: str, stations: List[str]):
        self._name = name
        self._stations = stations
        self._memphis: Memphis = Memphis()

    async def publish_event(self, event: Event):
        if self._producer is None:
            memphis: Memphis = Memphis()
            str_acct_id = os.getenv('MEMPHIS_ACCOUNT_ID')
            account_id = 0
            host = os.getenv('MEMPHIS_HOST') or ''
            username = os.getenv('MEMPHIS_USERNAME') or ''
            password = os.getenv('MEMPHIS_PASSWORD') or ''
            if str_acct_id is not None:
                account_id = int(str_acct_id)
            await memphis.connect(
                host=host,
                username=username,
                password=password,
                account_id=account_id
            )
            for station in self._stations:
                await memphis.station(station)
            self._producer = await memphis.producer(self._stations, f'{self._name}-{uuid4()}')
        headers = Headers()
        headers.add('Event-Type', event.__class__.__module__)
        await self._producer.produce(message=event.model_dump(), headers=headers)
```

This router pushes the event to Memphis.dev message broker and awaits confirmation
that the event was received.

## Project Structure

There are parts of this architecture that require a predictable packaging
of the application.
Aggregates should be stored in their own package with the same name
as the aggregate. 
E.g., `Election` is stored in `PhotoVote.Domain.Election`, along with the
DDD classes that compose it, such as `ElectionName` and `ElectionId`.
There will be a corresponding `Events` package for each aggregate, in which
all related `Event` classes will be placed.

src
+ PhotoVote
  + Domain
  + Event
  + Exception
+ server
  + routers
+ worker
  + eventstoredb
  + cosmosdb

Domain classes and event classes go under `PhotoVote/Domain` and
`PhotoVote/Event` respectively. 
Any classes that extend `Exception` will go under `Exception`.

Additional routers go under `server/routers`.

The eventstore worker and cosmosdb worker go under their respective
directories in `worker`, along with any supporting classes.

## Conclusion

Let's recap what we've seen here:
1. DDD Design and Event Sourcing to generate classes and properties
2. Conventions to be followed for aggregates, properties and events
3. How to write a modular FastAPI API
4. How to send events to Memphis.dev

This completes the API portion of the application. 
It is quickly extended by adding new aggregates, properties, and
events.
The API is designed to be modified to handle new events and aggregates,
since the code to do so is reusable.

## EventStore

With the event now passed off to the message broker, there are options
on how to deal with the event.
The audit benefits mentioned above are quite important in many industries
and are slowly becoming regulated to this degree.
In an age of AI, compliance in any tech-heavy industry is going to be
important, regardless of what the law is.
To be responsible to customers, a company must be able to answer the basic
questions of Who, What, When, Where, Why.
More importantly, they must have a high degree of confidence that their
records are correct.
While this could be expanded at great length, suffice it to say that it is
important to have an Authoritative Data Source that is immutable and reliable.
EventStoreDB is a unique solution that does just that: it can easily
be inserted into a message pipeline and persist everything that comes
through it permanently.
It is specifically designed for an event-driven architecture, and 
documents very well how to do so (in multiple languages and frameworks).

## EventStore Worker

This application is simplified by only needing a single EventStore worker.
In a larger application, there would be a worker required for each aggregate
root (i.e., each DDD domain).
However, the generic EventStoreDB functionality is a good candidate
for reuse. 
Multiple worker threads can be started with just a few configuration
variables.

The essential function of this worker is to:
1. Receive messages bound for the 'election' Memphis station
2. Determine the aggregate root the message belongs to
3. Store the event in EventStoreDB in the appropriately named stream.

The complete source code for `EventStoreWorker` is a bit long, so I'll
focus here on just the portion that receives events from Memphis and writes
them to EventStore.

```python
from typing import List
from memphis import Memphis, MemphisError
from memphis.message import Message

import json

async def process_messages(self, msgs: List[Message], error: MemphisError, context: Memphis) -> None:
        # The error only tells us that the last consume timed out and there's nothing to do
        # It does not seem to be possible to receive both messages and the MemphisError indicating that
        # the last consume() timed out. Presumably this was done to allow restarting the consume without
        # resorting to more complex alternatives.
        for msg in msgs:
            if not error:
                data = msg.get_data().decode("utf-8")
                obj = json.loads(data)
                if not obj["id"]:
                    raise ValueError("Event id is required")
                headers = msg.get_headers()
                event = self._create_event_instance(headers.get("Event-Type"), obj["id"], data)
                await self.write_to_eventstore(event)
                await msg.ack()
            else:
                await msg.nack()
```

Here, the event is reconstructed from the JSON so it can be passed into the
`write_to_eventstore()` method. 
It is not strictly necessary to do so; the JSON could be passed also and
treated as a `Dict`.
The JSON is missing the type information, though, so it would have to be
passed separately, anyway. 
Reconstructing the event is more readable and flexible.

Here is the `write_to_eventstore()` method as well:

```python
from PhotoVote.Event import Event
from esdbclient import NewEvent, StreamState
from uuid import uuid4


async def write_to_eventstore(self, event: Event) -> None:
        try:
            election_id = getattr(event, 'election_id')
            if election_id is None:
                raise ValueError("No election id in event")
            # All events fall under the Election aggregate root. There is no need to also write the
            # other aggregates to their own streams, since they don't stand on their own outside the
            # context of the election to which they belong.
            stream_name = f'Election-{election_id}'
            # There's not much point in loading the event stream since we'll end up just taking the count
            # of items in there as authoritative. Therefore, the fastest approach is to append to the end of the
            # stream blindly. If there were additional validation sources, we could load the aggregate here and
            # do validations here before appending to the stream.
            self.esdb.append_to_stream(stream_name, current_version=StreamState.ANY,
                                       events=[NewEvent(
                                           id=uuid4(),
                                           data=event.model_dump_json().encode('utf8'),
                                           type=event.__class__.__module__)])
        except Exception as ex:
            raise RuntimeError(f"Error: Unable to write to eventstore: {ex}")
```

We determine the stream name and write it to EventStore verbatim.
In a more complex application, `EventStoreWorker` would be a generic
class and the stream name calculated from the generic type of the worker.
In this case, it would also be necessary to start a thread for each
EventStore worker. 
As this would introduce additional complexity, it will not be covered
in this demonstration.

### Conclusion

`EventStoreWorker` is simple by design.
It cannot be denied that there will be additional latency introduced by
this step, so minimizing its impact is important.
However, the benefits far outweigh the small latency, and it is mitigated
by application design (more on that later).

## CosmosDB