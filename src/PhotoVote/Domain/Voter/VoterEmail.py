from pydantic import RootModel


class VoterEmail(RootModel):
    def __init__(self, email: str):
        super().__init__(email)

    def __str__(self):
        return self.root
