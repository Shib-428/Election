from pydantic import BaseModel

class DistrictVoteSchema(BaseModel):
    candidate_id: int
    prefecture: str
    district: int
    votes: int

    class Config:
        from_attributes = True