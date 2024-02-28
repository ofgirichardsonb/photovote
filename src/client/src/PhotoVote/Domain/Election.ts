import {Competition} from "./Competition";
import {Ballot} from "./Ballot";
import {Voter} from "./Voter";
import {Aggregate} from "./Aggregate";

class Election extends Aggregate {
    public name?: string;
    public description?: string;
    public competitions: Competition[] = []
    public ballots: Ballot[] = []
    public voters: Voter[] = []

    constructor(id: string) {
        super(id);
    }
}

export { Election }