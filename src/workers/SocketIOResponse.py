from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class SocketIOResponse(BaseModel):
    request_id: str
    recipient: str = Field(default=None)
    success: bool = Field(default=False)
    message: Optional[str] = None
    error: Optional[str] = None
    data: Any = Field(default=None)
