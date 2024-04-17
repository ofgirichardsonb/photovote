import uuid
from typing import Optional

from pydantic import BaseModel, Field


class MemphisRequest(BaseModel):
    request_id: str
    reply_to: Optional[str] = None
    access_token: Optional[str] = None
