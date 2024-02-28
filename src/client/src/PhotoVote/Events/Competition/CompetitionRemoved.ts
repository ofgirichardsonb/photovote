import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CompetitionRemoved extends Event {
    competitionId?: string
    electionId?: string

    constructor() {
        super(randomUUID());
    }
}

export { CompetitionRemoved }