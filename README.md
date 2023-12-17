# photovote
A simple Python FastAPI application demonstrating Event-Driven Architecture and Domain-Driven Design

# Details

An Election is a simple Domain with only 5 identified Aggregate Roots:

* Election
* Competition
* Candidate
* Ballot
* Voter

This package provides the source for all Aggregate Roots, including a base `AggregateRoot` class, as well
as base `Event` and `AggregateId` classes.

This application was developed using techniques from Domain-Driven Design and Event Sourcing, and is sufficiently
&emdash; but not excessively &emdash; complex to demonstrate how all of the pieces fit together.

Currently, the application uses [Memphis.dev](https://memphis.dev), a cloud-based message broker that is both powerful and
easy to use. [EventStoreDB](https://eventstore.com) is used for long-term event storage separated into individual event
streams by individual Aggregate Root. MongoDB is used as a read cache for the API.

The application runs as a FastAPI application. If you wish to run it, you will need:

* A local Memphis.dev installation or a cloud-based Memphis.dev account
* A local EventStoreDB installation or a cloud-based EventStoreDB account
* A local MongoDB installation or a cloud-based (Atlas, e.g.) MongoDB account

You will need to put the details of your installations into the `.env` file, which you can copy from `example-env`
