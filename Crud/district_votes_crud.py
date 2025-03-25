from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Model import DistrictVoteModel
from Schema import DistrictVoteCreateSchema, DistrictVoteUpdateSchema

async def db_create_district_vote(db: AsyncSession, district_vote: DistrictVoteCreateSchema) -> DistrictVoteModel:
    db_district_vote = DistrictVoteModel(
        candidate_id=district_vote.candidate_id,
        prefecture=district_vote.prefecture,
        district=district_vote.district,
        votes=district_vote.votes
    )
    db.add(db_district_vote)
    await db.commit()
    await db.refresh(db_district_vote)
    return db_district_vote

async def db_get_district_vote(db: AsyncSession, candidate_id: int) -> DistrictVoteModel | None:
    result = await db.execute(select(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == candidate_id))
    return result.scalars().first()

async def db_get_district_votes(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[DistrictVoteModel]:
    results = await db.execute(select(DistrictVoteModel).offset(skip).limit(limit))
    return results.scalars().all()

async def db_update_district_vote(db: AsyncSession, candidate_id: int, updated_district_vote: DistrictVoteUpdateSchema) -> DistrictVoteModel | None:
    result = await db.execute(select(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == candidate_id))
    db_district_vote = result.scalars().first()
    if db_district_vote:
        db_district_vote.candidate_id = updated_district_vote.candidate_id
        db_district_vote.prefecture = updated_district_vote.prefecture
        db_district_vote.district = updated_district_vote.district
        db_district_vote.votes = updated_district_vote.votes
        await db.commit()
        await db.refresh(db_district_vote)
    return db_district_vote

async def db_delete_district_vote(db: AsyncSession, candidate_id: int) -> DistrictVoteModel | None:
    result = await db.execute(select(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == candidate_id))
    db_district_vote = result.scalars().first()
    if db_district_vote:
        await db.delete(db_district_vote)
        await db.commit()
    return db_district_vote