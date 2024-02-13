from PhotoVote.Domain import AggregateId


class CompetitionId(AggregateId):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
