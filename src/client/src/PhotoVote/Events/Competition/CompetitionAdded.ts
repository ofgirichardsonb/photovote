import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CompetitionAdded extends Event {
    competitionId?: string
    electionId?: string
    name?: string
    description?: string

    constructor() {
        super(randomUUID());
    }
}

export { CompetitionAdded }