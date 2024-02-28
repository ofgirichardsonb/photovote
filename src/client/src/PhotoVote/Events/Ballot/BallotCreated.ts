import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class BallotCreated extends Event {
    electionId?: string
    ballotId?: string
    // Unfortunately, we need to include voterId here so that we can verify that the voter has
    // been registered. It would require some decent cryptography to avoid this requirement.
    voterId?: string

    constructor() {
        super(randomUUID())
    }
}

export { BallotCreated }