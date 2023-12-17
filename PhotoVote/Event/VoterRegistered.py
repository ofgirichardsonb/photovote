from Common.Event import Event


class VoterRegistered(Event):
    name: str
    email: str
