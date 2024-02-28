import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CandidateImageChanged extends Event {
    candidateId?: string
    competitionId?: string
    electionId?: string
    imageUrl?: string
    imageCaption?: string

    constructor() {
        super(randomUUID());
    }
}

export { CandidateImageChanged }