from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from Crud import db_get_district_vote, db_get_district_votes, db_create_district_vote, db_update_district_vote, db_delete_district_vote
from Schema import DistrictVoteSchema, DistrictVoteCreateSchema, DistrictVoteUpdateSchema
from database import get_db

router = APIRouter()

""" CRUD操作のルーティング """
""" 新規作成 """
@router.post("/", response_model=DistrictVoteSchema)
def create_new_district_vote(
    district_vote: DistrictVoteCreateSchema,
    db: Session = Depends(get_db)
) -> DistrictVoteSchema:
    return db_create_district_vote(db, district_vote)

""" 一覧表示 """
@router.get("/", response_model=list[DistrictVoteSchema])
def read_district_votes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[DistrictVoteSchema]:
    return db_get_district_votes(db, skip, limit)

""" 詳細表示 """
@router.get("/{candidate_id}", response_model=DistrictVoteSchema)
def read_district_vote(candidate_id: int, db: Session = Depends(get_db)) -> DistrictVoteSchema:
    db_district_vote = db_get_district_vote(db, candidate_id)
    if db_district_vote is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_district_vote

""" 編集 """
@router.put("/{candidate_id}", response_model=DistrictVoteSchema)
def update_existing_district_vote(candidate_id: int, district_vote: DistrictVoteUpdateSchema, db: Session = Depends(get_db)):
    db_district_vote = db_update_district_vote(db, candidate_id, district_vote)
    if db_district_vote is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_district_vote

""" 削除 """
@router.delete("/{id}", response_model=DistrictVoteSchema)
def delete_existing_district_vote(candidate_id: int, db: Session = Depends(get_db)) -> DistrictVoteSchema:
    db_district_vote = db_delete_district_vote(db, candidate_id)
    if db_district_vote is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_district_vote