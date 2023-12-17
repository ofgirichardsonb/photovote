from Common.Event import Event


class CandidateNameChanged(Event):
    name: str
