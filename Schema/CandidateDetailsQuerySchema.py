from pydantic import BaseModel
from .CandidateSchema import CandidateSchema
from .DistrictVoteSchema import DistrictVoteSchema

class CandidateDetailsQuerySchema(BaseModel):
    candidate: CandidateSchema | None
    district_vote: DistrictVoteSchema | None