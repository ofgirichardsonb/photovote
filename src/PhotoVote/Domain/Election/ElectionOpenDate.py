from datetime import datetime

from pydantic import RootModel


class ElectionOpenDate(RootModel):
    def __init__(self, open_date: datetime):
        super().__init__(open_date)

    def __eq__(self, other):
        if isinstance(other, ElectionOpenDate):
            return self.root == other.root
        elif isinstance(other, datetime):
            return self.root == other
        return False

    def __gt__(self, other):
        if isinstance(other, ElectionOpenDate):
            return self.root > other.root
        elif isinstance(other, datetime):
            return self.root > other
        return False

    def __lt__(self, other):
        if isinstance(other, ElectionOpenDate):
            return self.root < other.root
        elif isinstance(other, datetime):
            return self.root < other
        return False
