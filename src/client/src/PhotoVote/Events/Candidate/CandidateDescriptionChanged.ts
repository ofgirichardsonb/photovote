import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CandidateDescriptionChanged extends Event {
    candidateId?: string
    competitionId?: string
    electionId?: string
    description?: string

    constructor() {
        super(randomUUID())
    }
}

export { CandidateDescriptionChanged }