from typing import Optional
from Common.Event import Event


class ElectionDescriptionChanged(Event):
    description: str
