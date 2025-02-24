from pydantic import BaseModel

class PostCandidateSchema(BaseModel):
    id: int
    name: str
    party: str
    win_count: int