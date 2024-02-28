import {Event} from '../Event'
import {randomUUID} from "node:crypto";

class ElectionDescriptionChanged extends Event {
    electionId?: string
    description?: string

    constructor() {
        super(randomUUID());
    }
}

export { ElectionDescriptionChanged }