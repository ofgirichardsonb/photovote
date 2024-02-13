from pydantic import RootModel


class CandidateDescription(RootModel):
    def __init__(self, description: str):
        super().__init__(description)
