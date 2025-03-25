from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Crud import db_get_candidate, db_get_candidates, db_create_candidate, db_update_candidate, db_delete_candidate
from Query import get_candidate_details
from Schema import CandidateSchema, CandidateCreateSchema, CandidateUpdateSchema, CandidateDetailsResponseSchema
from database import get_db

router = APIRouter()

@router.post("/", response_model=CandidateSchema)
async def create_new_candidate(
        candidate: CandidateCreateSchema, 
        db: AsyncSession = Depends(get_db)
    ) -> CandidateSchema:
    # 受け取ったデータからモデルを作成
    return await db_create_candidate(db, candidate)

@router.get("/", response_model=list[CandidateSchema])
async def read_candidates(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)) -> list[CandidateSchema]:
    return await db_get_candidates(db, skip, limit)

@router.get("/{candidate_id}", response_model=CandidateSchema)
async def read_candidate(candidate_id: int, db: AsyncSession = Depends(get_db)) -> CandidateSchema:
    db_candidate = await db_get_candidate(db, candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/{candidate_id}", response_model=CandidateSchema)
async def update_existing_candidate(candidate_id: int, candidate: CandidateUpdateSchema, db: AsyncSession = Depends(get_db)):
    db_candidate = await db_update_candidate(db, candidate_id, candidate)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.delete("/{id}", response_model=CandidateSchema)
async def delete_existing_candidate(candidate_id: int, db: AsyncSession = Depends(get_db)) -> CandidateSchema:
    db_candidate = await db_delete_candidate(db, candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

""" 非CRUD操作のルーティング """
@router.get("/details/{id}", response_model=CandidateDetailsResponseSchema)
async def get_candidate(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> CandidateDetailsResponseSchema:
    result = await get_candidate_details(db, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Both Candidate and District Vote not found")
    candidate = result.candidate
    district_vote = result.district_vote
    
    return CandidateDetailsResponseSchema(
        id=candidate.id if candidate else 'no data',
        name=candidate.name if candidate else 'no data',
        party=candidate.party if candidate else 'no data',
        win_count=candidate.win_count if candidate else 'no data',
        prefecture=district_vote.prefecture if district_vote else 'no data',
        district=district_vote.district if district_vote else 'no data',
        votes=district_vote.votes if district_vote else 'no data'
    )