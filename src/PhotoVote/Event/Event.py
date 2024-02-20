from pydantic import BaseModel


# The base model for all events, requires only a unique identifier (of any string representation)
# Additional attributes for each subclass _must be Optional_. It is necessary to create empty events prior
# loading them from JSON.
class Event(BaseModel):
    id: str
