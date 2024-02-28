import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class BallotCandidateRated extends Event {
    constructor() {
        super(randomUUID())
    }
}

export { BallotCandidateRated }