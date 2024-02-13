from PhotoVote.Domain import AggregateId


class ElectionId(AggregateId):
    def __init__(self, election_id: str):
        super().__init__(election_id)
