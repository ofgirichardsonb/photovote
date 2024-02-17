from pydantic import RootModel


class Rating(RootModel):
    def __init__(self, rating: int):
        super().__init__(rating)

    def __int__(self):
        return self.root
