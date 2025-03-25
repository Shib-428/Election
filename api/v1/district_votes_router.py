from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from Crud import db_get_district_vote, db_get_district_votes, db_create_district_vote, db_update_district_vote, db_delete_district_vote
from Schema import DistrictVoteCreateSchema, DistrictVoteUpdateSchema
from Response import SuccessResponseSchema, ErrorResponseSchema
from database import get_db

router = APIRouter()

""" CRUD操作のルーティング """
""" 新規作成 """
@router.post("/", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def create_new_district_vote(
    district_vote: DistrictVoteCreateSchema,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    results = await db_create_district_vote(db, district_vote)
    return SuccessResponseSchema(
        code=201,
        results=results
    )

""" 一覧表示 """
@router.get("/", response_model=SuccessResponseSchema)
async def read_district_votes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema:
    results = await db_get_district_votes(db, skip, limit)
    return SuccessResponseSchema(
        code=200,
        results=results
    )

""" 詳細表示 """
@router.get("/{candidate_id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def read_district_vote(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_district_vote = await db_get_district_vote(db, candidate_id)
    if db_district_vote:
        return SuccessResponseSchema(
            code=200,
            results=db_district_vote
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"District Vote (Candidate id: {candidate_id}) not found"
        )

""" 編集 """
@router.put("/{candidate_id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def update_existing_district_vote(
    candidate_id: int,
    district_vote: DistrictVoteUpdateSchema,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_district_vote = await db_update_district_vote(db, candidate_id, district_vote)
    if db_district_vote:
        return SuccessResponseSchema(
            code=201,
            results=db_district_vote
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"District Vote (Candidate id: {candidate_id}) not found"
        )

""" 削除 """
@router.delete("/{id}", response_model=SuccessResponseSchema | ErrorResponseSchema)
async def delete_existing_district_vote(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponseSchema | ErrorResponseSchema:
    db_district_vote = await db_delete_district_vote(db, candidate_id)
    if db_district_vote:
        return SuccessResponseSchema(
            code=204,
            results=db_district_vote
        )
    else:
        return ErrorResponseSchema(
            code=404,
            message=f"District Vote (Candidate id: {candidate_id}) not found"
        )