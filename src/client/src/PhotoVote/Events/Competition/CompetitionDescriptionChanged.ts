import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CompetitionDescriptionChanged extends Event {
    competitionId?: string
    electionId?: string
    description?: string

    constructor() {
        super(randomUUID());
    }
}

export { CompetitionDescriptionChanged }