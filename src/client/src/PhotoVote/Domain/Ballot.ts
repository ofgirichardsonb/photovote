import {Aggregate} from "./Aggregate";

type RatingType = {
    [id: string]: {
        [id: string]: number
    }
};

class Ballot extends Aggregate {
    public electionId: string
    public ratings: RatingType = { }


    constructor(id: string, electionId: string) {
        super(id)
        this.electionId = electionId;
    }
}

export { Ballot }