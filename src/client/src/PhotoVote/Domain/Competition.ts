import {Candidate} from "./Candidate";
import {Aggregate} from "./Aggregate";

class Competition extends Aggregate {
    public electionId: string
    public name?: string
    public description?: string
    public candidates: Candidate[] = []

    constructor(id: string, electionId: string) {
        super(id);
        this.electionId = electionId;
    }
}

export { Competition }