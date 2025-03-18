from sqlalchemy.orm import Session
from Model import DistrictVoteModel
from Schema import DistrictVoteCreateSchema, DistrictVoteUpdateSchema

def db_create_district_vote(db: Session, district_vote: DistrictVoteCreateSchema) -> DistrictVoteModel:
    db_district_vote = DistrictVoteModel(
        candidate_id=district_vote.candidate_id,
        prefecture=district_vote.prefecture,
        district=district_vote.district,
        votes=district_vote.votes
    )
    db.add(db_district_vote)
    db.commit()
    db.refresh(db_district_vote)
    return db_district_vote

def db_get_district_vote(db: Session, candidate_id: int) -> DistrictVoteModel | None:
    return db.query(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == candidate_id).first()

def db_get_district_votes(db: Session, skip: int = 0, limit: int = 10) -> list[DistrictVoteModel]:
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(DistrictVoteModel).offset(skip).limit(limit).all()

def db_update_district_vote(db: Session, candidate_id: int, district_vote: DistrictVoteUpdateSchema) -> DistrictVoteModel:
    db_district_vote = db.query(DistrictVoteModel).filter(DistrictVoteModel.id == candidate_id).first()
    if db_district_vote:
        db_district_vote.candidate_id = district_vote.candidate_id
        db_district_vote.prefecture = district_vote.prefecture
        db_district_vote.district = district_vote.district
        db_district_vote.votes = district_vote.votes
        db.commit()
        db.refresh(db_district_vote)
    return db_district_vote

def db_delete_district_vote(db: Session, candidate_id: int) -> DistrictVoteModel:
    db_district_vote = db.query(DistrictVoteModel).filter(DistrictVoteModel.candidate_id == candidate_id).first()
    if db_district_vote:
        db.delete(db_district_vote)
        db.commit()
    return db_district_vote