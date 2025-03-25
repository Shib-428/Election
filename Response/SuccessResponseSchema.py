from pydantic import BaseModel

from Schema import CandidateSchema, DistrictVoteSchema, CandidateDetailsResponseSchema

class SuccessResponseSchema(BaseModel):
    code: int
    results: CandidateSchema | DistrictVoteSchema | CandidateDetailsResponseSchema | list[CandidateSchema | DistrictVoteSchema]