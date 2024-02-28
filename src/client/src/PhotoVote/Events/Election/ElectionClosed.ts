import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionClosed extends Event {
    electionId?: string
    closed?: Date

    constructor() {
        super(randomUUID());
    }
}

export { ElectionClosed }