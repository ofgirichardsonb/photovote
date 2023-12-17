from __future__ import annotations


class Rating:

    def __init__(self, rating: int):
        self._value: int = rating

    def __int__(self) -> int:
        return self._value

    @staticmethod
    def from_int(value: int) -> Rating:
        return Rating(value)

