class AlreadyDeletedError(Exception):
    def __init__(self):
        super().__init__("Aggregate has been deleted")
