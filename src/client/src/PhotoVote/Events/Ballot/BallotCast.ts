import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class BallotCast extends Event {
    ballotId?: string
    electionId?: string

    constructor() {
        super(randomUUID());
    }
}

export { BallotCast }