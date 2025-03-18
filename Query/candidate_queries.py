from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Model import CandidateModel, DistrictVoteModel
from Schema import CandidateDetailsQuerySchema

async def get_candidate_details(db: AsyncSession, id: int) -> CandidateDetailsQuerySchema | None:
    candidate_result = await db.execute(select(CandidateModel).filter(CandidateModel.id == id))
    candidate = candidate_result.scalars().first()

    district_vote_result = await db.execute(select(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == id))
    district_vote = district_vote_result.scalars().first()
    
    return CandidateDetailsQuerySchema(candidate=candidate, district_vote=district_vote) if any([candidate, district_vote]) else None