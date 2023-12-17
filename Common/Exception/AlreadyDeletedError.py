class AlreadyDeletedError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self._message: str = message

    def __str__(self):
        return self._message

    @property
    def message(self):
        return self._message
