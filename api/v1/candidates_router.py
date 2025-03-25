from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from Crud import db_get_candidate, db_get_candidates, db_create_candidate, db_update_candidate, db_delete_candidate
from Query import get_candidate_details
from Schema import CandidateCreateSchema, CandidateUpdateSchema, CandidateDetailsResponseSchema
from Response import SuccessResponseSchema, ErrorResponseSchema
from database import get_db

router = APIRouter()

@router.post("/", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def create_new_candidate(
        candidate: CandidateCreateSchema, 
        db: AsyncSession = Depends(get_db)
    ) -> SuccessResponseSchema | ErrorResponseSchema:
    # 受け取ったデータからモデルを作成
    results = await db_create_candidate(db, candidate)
    return SuccessResponseSchema(
        code=201,
        results=results
    )
    

@router.get("/", response_model=SuccessResponseSchema)
async def read_candidates(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema:
    results = await db_get_candidates(db, skip, limit)
    return SuccessResponseSchema(
        code=200,
        results=results
    )

@router.get("/{candidate_id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def read_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_candidate = await db_get_candidate(db, candidate_id)
    if db_candidate:
        return SuccessResponseSchema(
            code=200,
            results=db_candidate
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"Candidate (id: {candidate_id}) not found"
        )

@router.put("/{candidate_id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def update_existing_candidate(
    candidate_id: int,
    updated_candidate: CandidateUpdateSchema,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_candidate = await db_update_candidate(db, candidate_id, updated_candidate)
    if db_candidate:
        return SuccessResponseSchema(
            code=201,
            results=db_candidate
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"Candidate (id: {candidate_id}) not found"
        )

@router.delete("/{id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def delete_existing_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_candidate = await db_delete_candidate(db, candidate_id)
    if db_candidate:
        return SuccessResponseSchema(
            code=204,
            results=db_candidate
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"Candidate (id: {candidate_id}) not found"
        )

""" 非CRUD操作のルーティング """
@router.get("/details/{id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def get_candidate(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    results = await get_candidate_details(db, id)
    if results:
        candidate = results.candidate
        district_vote = results.district_vote
        return SuccessResponseSchema(
            code=200,
            results=CandidateDetailsResponseSchema(
                id=candidate.id if candidate else 'no data',
                name=candidate.name if candidate else 'no data',
                party=candidate.party if candidate else 'no data',
                win_count=candidate.win_count if candidate else 'no data',
                prefecture=district_vote.prefecture if district_vote else 'no data',
                district=district_vote.district if district_vote else 'no data',
                votes=district_vote.votes if district_vote else 'no data'
            )
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"Both Candidate and District Vote not found")