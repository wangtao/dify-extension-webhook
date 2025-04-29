from pydantic import BaseModel


class MRUser(BaseModel):
    id: int
    name: str
    username: str


class AppRequestMessage(BaseModel):
    project_id: str
    iid: str
    category: str
    query: str
    user: str


class AppResponseMessage(BaseModel):
    answer: str
    conversation_id: str
