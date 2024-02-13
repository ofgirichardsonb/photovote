class VoterNotRegisteredError(Exception):
    def __init__(self):
        super().__init__("Voter has not been registered")
