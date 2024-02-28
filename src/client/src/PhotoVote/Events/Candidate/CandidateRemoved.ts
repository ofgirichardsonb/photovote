import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CandidateRemoved extends Event {
    candidateId?: string
    competitionId?: string
    electionId?: string

    constructor() {
        super(randomUUID());
    }
}

export { CandidateRemoved }