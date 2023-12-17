from typing import Optional
from Common.Event import Event


class CandidateImageCaptionChanged(Event):
    caption: Optional[str]

