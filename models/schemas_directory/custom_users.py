from pydantic import BaseModel


class CustomUsers(BaseModel):
    username: str
    password: str
    id: int

    class Config:
        orm_mode = True
