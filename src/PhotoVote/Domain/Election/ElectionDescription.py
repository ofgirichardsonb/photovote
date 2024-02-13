from pydantic import RootModel


class ElectionDescription(RootModel):
    def __init__(self, description: str):
        super().__init__(description)

    def __str__(self):
        return self.root
