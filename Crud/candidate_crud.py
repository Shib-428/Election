from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Model import CandidateModel
from Schema import CandidateCreateSchema, CandidateUpdateSchema

async def db_create_candidate(db: AsyncSession, candidate: CandidateCreateSchema) -> CandidateModel:
    db_candidate = CandidateModel(
        id=candidate.id,
        name=candidate.name,
        party=candidate.party,
        win_count=candidate.win_count
    )
    db.add(db_candidate)
    await db.commit() # 非同期コミット
    await db.refresh(db_candidate) # 非同期リフレッシュ
    return db_candidate

async def db_get_candidate(db: AsyncSession, candidate_id: int) -> CandidateModel | None:
    result = await db.execute(select(CandidateModel).filter(CandidateModel.id == candidate_id))
    return result.scalars().first()

async def db_get_candidates(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[CandidateModel]:
    result = await db.execute(select(CandidateModel).offset(skip).limit(limit))
    return result.scalars().all()

async def db_update_candidate(db: AsyncSession, candidate_id: int, candidate: CandidateUpdateSchema) -> CandidateModel | None:
    # 非同期でクエリを実行
    result = await db.execute(select(CandidateModel).filter(CandidateModel.id == candidate_id))
    db_candidate = result.scalars().first()
    if db_candidate:
        db_candidate.name = candidate.name
        db_candidate.party = candidate.party
        db_candidate.win_count = candidate.win_count
        await db.commit()  # 非同期コミット
        await db.refresh(db_candidate)  # 非同期リフレッシュ
    return db_candidate

async def db_delete_candidate(db: AsyncSession, candidate_id: int) -> CandidateModel | None:
    # 非同期でクエリを実行
    result = await db.execute(select(CandidateModel).filter(CandidateModel.id == candidate_id))
    db_candidate = result.scalars().first()
    if db_candidate:
        await db.delete(db_candidate)  # 非同期削除
        await db.commit()  # 非同期コミット
    return db_candidate