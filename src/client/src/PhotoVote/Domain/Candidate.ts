import {CandidateImage} from "./CandidateImage";
import {Aggregate} from "./Aggregate";

class Candidate extends Aggregate {
    public electionId: string;
    public competitionId: string;
    public name?: string;
    public description?: string;
    public image?: CandidateImage;

    constructor(id: string, electionId: string, competitionId: string) {
        super(id)
        this.electionId = electionId;
        this.competitionId = competitionId;
    }
}

export { Candidate }