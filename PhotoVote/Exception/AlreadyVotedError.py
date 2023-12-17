class AlreadyVotedError(Exception):
    @property
    def message(self):
        return self._message

    def __init__(self, message: str):
        super().__init__()
        self._message: str = message

    def __str__(self) -> str:
        return self._message
