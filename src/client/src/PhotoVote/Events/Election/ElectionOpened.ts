import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionOpened extends Event {
    electionId?: string
    opened?: Date

    constructor() {
        super(randomUUID());
    }
}

export { ElectionOpened }