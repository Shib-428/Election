from pydantic import BaseModel

class CandidateUpdateSchema(BaseModel):
    name: str
    party: str
    win_count: int