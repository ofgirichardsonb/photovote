import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class VoterRegistered extends Event {
    voterId?: string
    electionId?: string
    name?: string
    email?: string

    constructor() {
        super(randomUUID());
    }
}

export { VoterRegistered }