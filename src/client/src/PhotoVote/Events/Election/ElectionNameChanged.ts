import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionNameChanged extends Event {
    electionId?: string
    name?: string

    constructor() {
        super(randomUUID());
    }
}

export { ElectionNameChanged }