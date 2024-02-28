import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionDeleted extends Event {
    electionId?: string

    constructor() {
        super(randomUUID());
    }
}

export { ElectionDeleted }