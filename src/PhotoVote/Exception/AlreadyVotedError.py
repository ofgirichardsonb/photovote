class AlreadyVotedError(Exception):
    def __init__(self):
        super().__init__("Ballot has already been cast")
