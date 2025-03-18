from pydantic import BaseModel
from .CandidateSchema import CandidateSchema
from .DistrictVoteSchema import DistrictVoteSchema

class CandidateDetailsQuerySchema(BaseModel):
    candidate: CandidateSchema
    district_vote: DistrictVoteSchema