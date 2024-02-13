from datetime import datetime

from pydantic import RootModel


class ElectionCloseDate(RootModel):
    def __init__(self, close_date: datetime):
        super().__init__(close_date)

    def __eq__(self, other):
        if isinstance(other, ElectionCloseDate):
            return self.root == other.root
        elif isinstance(other, datetime):
            return self.root == other
        return False

    def __gt__(self, other):
        if isinstance(other, ElectionCloseDate):
            return self.root > other.root
        elif isinstance(other, datetime):
            return self.root > other
        return False

    def __lt__(self, other):
        if isinstance(other, ElectionCloseDate):
            return self.root < other.root
        elif isinstance(other, datetime):
            return self.root < other
        return False
