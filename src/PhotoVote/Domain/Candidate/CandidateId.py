from PhotoVote.Domain import AggregateId


class CandidateId(AggregateId):
    def __init__(self, candidate_id: str):
        super().__init__(candidate_id)

