from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostBaseWitID(BaseModel):
    id: int
    title: str
    content: str


class LikeBase(BaseModel):
    id: int
    post_id: int
