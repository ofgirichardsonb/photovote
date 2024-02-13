from pydantic import RootModel


class ImageCaption(RootModel):
    def __init__(self, caption: str):
        super().__init__(caption)

    def __str__(self):
        return self.root
