import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CandidateAdded extends Event {
    candidateId?: string
    competitionId?: string
    electionId?: string
    name?: string
    description?: string
    imageUrl?: string
    imageCaption?: string

    constructor() {
        super(randomUUID());
    }
}

export { CandidateAdded }