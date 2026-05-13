from pydantic import BaseModel

class Player(BaseModel):
    name: str
    position: str
    number: int