from pydantic import RootModel


class ImageUrl(RootModel):
    def __init__(self, url: str):
        super().__init__(url)

    def __str__(self):
        return self.root
