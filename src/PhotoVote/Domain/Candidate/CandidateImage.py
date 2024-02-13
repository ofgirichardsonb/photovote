from typing import Optional

from pydantic import BaseModel

from PhotoVote.Domain.Candidate import ImageCaption, ImageUrl


class CandidateImage(BaseModel):
    url: ImageUrl
    caption: Optional[ImageCaption]
