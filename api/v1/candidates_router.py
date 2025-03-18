from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from Crud import db_get_candidate, db_get_candidates, db_create_candidate, db_update_candidate, db_delete_candidate
from Query import get_candidate_details
from Schema import CandidateSchema, CandidateCreateSchema, CandidateUpdateSchema, CandidateDetailsResponseSchema
from database import get_db

router = APIRouter()

""" CRUD操作のルーティング """
@router.post("/", response_model=CandidateSchema)
def create_new_candidate(
        candidate: CandidateCreateSchema, 
        db: Session = Depends(get_db)
    ) -> CandidateSchema:
    # 受け取ったデータからモデルを作成
    return db_create_candidate(db, candidate)

@router.get("/", response_model=list[CandidateSchema])
def read_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[CandidateSchema]:
    return db_get_candidates(db, skip, limit)

@router.get("/{candidate_id}", response_model=CandidateSchema)
def read_candidate(candidate_id: int, db: Session = Depends(get_db)) -> CandidateSchema:
    db_candidate = db_get_candidate(db, candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/{candidate_id}", response_model=CandidateSchema)
def update_existing_candidate(candidate_id: int, candidate: CandidateUpdateSchema, db: Session = Depends(get_db)):
    db_candidate = db_update_candidate(db, candidate_id, candidate)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate


@router.delete("/{id}", response_model=CandidateSchema)
def delete_existing_candidate(candidate_id: int, db: Session = Depends(get_db)) -> CandidateSchema:
    db_candidate = db_delete_candidate(db, candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

""" 非CRUD操作のルーティング """
@router.get("/details/{id}", response_model=CandidateDetailsResponseSchema)
def get_candidate(
    id: int,
    db: Session = Depends(get_db)
) -> CandidateDetailsResponseSchema:
    result = get_candidate_details(db, id)
    candidate = result.candidate
    district_vote = result.district_vote
    return CandidateDetailsResponseSchema(
        id=candidate.id,
        name=candidate.name,
        party=candidate.party,
        win_count=candidate.win_count,
        prefecture=district_vote.prefecture,
        district=district_vote.district,
        votes=district_vote.votes
    )