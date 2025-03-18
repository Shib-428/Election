from sqlalchemy.orm import Session
from Model import CandidateModel
from Schema import CandidateCreateSchema, CandidateUpdateSchema

def db_create_candidate(db: Session, candidate: CandidateCreateSchema) -> CandidateModel:
    db_candidate = CandidateModel(
        id=candidate.id,
        name=candidate.name,
        party=candidate.party,
        win_count=candidate.win_count
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def db_get_candidate(db: Session, candidate_id: int) -> CandidateModel | None:
    return db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()

def db_get_candidates(db: Session, skip: int = 0, limit: int = 10) -> list[CandidateModel]:
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(CandidateModel).offset(skip).limit(limit).all()

def db_update_candidate(db: Session, candidate_id: int, candidate: CandidateUpdateSchema) -> CandidateModel | None:
    db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if db_candidate:
        db_candidate.name = candidate.name
        db_candidate.party = candidate.party
        db_candidate.win_count = candidate.win_count
        db.commit()
        db.refresh(db_candidate)
    return db_candidate

def db_delete_candidate(db: Session, candidate_id: int) -> CandidateModel | None:
    db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
    return db_candidate