import {Aggregate} from "./Aggregate";

class Voter extends Aggregate {
    public electionId: string;
    public name?: string;
    public email?: string;

    constructor(id: string, electionId: string) {
        super(id);
        this.electionId = electionId;
    }
}

export { Voter }