import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class CompetitionNameChanged extends Event {
    competitionId?: string
    electionId?: string
    name?: string

    constructor() {
        super(randomUUID());
    }
}

export { CompetitionNameChanged }