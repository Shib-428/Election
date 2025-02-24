from pydantic import BaseModel

class PostDistrictVoteSchema(BaseModel):
    candidate_id: int
    prefecture: str
    district: str
    votes: int