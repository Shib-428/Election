from fastapi import HTTPException
from Model import CandidateModel, DistrictVoteModel
from sqlalchemy.orm import Session

class CandidateQueries:
    @staticmethod
    def fetch_candidate_details(db: Session, id: int) -> dict[str: CandidateModel | DistrictVoteModel]:
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

        return {
            "candidate": candidate,
            "district_vote": district_vote
        }