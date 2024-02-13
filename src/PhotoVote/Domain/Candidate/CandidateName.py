from pydantic import RootModel


class CandidateName(RootModel):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return self.root