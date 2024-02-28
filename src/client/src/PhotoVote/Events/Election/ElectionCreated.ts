import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionCreated extends Event {
    electionId?: string
    name?: string
    description?: string

    constructor() {
        super(randomUUID());
    }
}

export { ElectionCreated }