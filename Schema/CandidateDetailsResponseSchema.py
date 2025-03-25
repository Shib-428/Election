from pydantic import BaseModel

class CandidateDetailsResponseSchema(BaseModel):
    id: int | str
    name: str
    party: str
    win_count: int | str
    prefecture: str # district_votes
    district: int | str # district_votes
    votes: int | str # district_votes