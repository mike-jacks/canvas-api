from pydantic import BaseModel

class Course(BaseModel):
    id: int
    name: str

class Discussion(BaseModel):
    id: int
    title: str
    discussion_type: str
    user_name: str