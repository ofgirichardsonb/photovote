from PhotoVote.Domain import AggregateId


class VoterId(AggregateId):
    def __init__(self, voter_id: str):
        super().__init__(voter_id)
