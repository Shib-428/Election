from pydantic import BaseModel

class DistrictVoteUpdateSchema(BaseModel):
    candidate_id: int
    prefecture: str
    district: int
    votes: int