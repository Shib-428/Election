from fastapi import HTTPException
from Model import CandidateModel, DistrictVoteModel
from Schema import CandidateDetailsQuerySchema
from sqlalchemy.orm import Session

def get_candidate_details(db: Session, id: int) -> CandidateDetailsQuerySchema:
    candidate = db.query(CandidateModel).filter(
        CandidateModel.id==id
    ).one()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    district_vote = db.query(DistrictVoteModel).filter(
        DistrictVoteModel.candidate_id==id
    ).one()
    if not district_vote:
        raise HTTPException(status_code=404, detail="District Vote not found")

    return CandidateDetailsQuerySchema(candidate=candidate, district_vote=district_vote)