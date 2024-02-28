import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CandidateNameChanged extends Event {
    candidateId?: string
    competitionId?: string
    electionId?: string
    name?: string

    constructor() {
        super(randomUUID());
    }
}

export { CandidateNameChanged }