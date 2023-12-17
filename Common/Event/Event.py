from pydantic import BaseModel


class Event(BaseModel):
    aggregate_id: str
