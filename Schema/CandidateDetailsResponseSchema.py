from pydantic import BaseModel

class CandidateDetailsResponseSchema(BaseModel):
    id: int
    name: str
    party: str
    win_count: int
    prefecture: str # district_votes
    district: int # district_votes
    votes: int # district_votes