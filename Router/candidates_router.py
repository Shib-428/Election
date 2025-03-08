from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from Model import CandidateModel
from Schema import PostCandidateSchema, CandidateDetailsResponseSchema
from Query import CandidateQueries
from database import get_db

router = APIRouter()

# データベースからCandidate一覧を取得するAPI
@router.get("/candidates")
def get_candidates(
        db: Session = Depends(get_db)
    ):
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(CandidateModel).all()

@router.get("/candidates/{id}", response_model=CandidateDetailsResponseSchema)
def get_candidate_details(
    id: int,
    db: Session = Depends(get_db)
):
    result = CandidateQueries.fetch_candidate_details(db, id)
    candidate = result['candidate']
    district_vote = result['district_vote']
    return CandidateDetailsResponseSchema(
        id=candidate.id,
        name=candidate.name,
        party=candidate.party,
        win_count=candidate.win_count,
        prefecture=district_vote.prefecture,
        district=district_vote.district,
        votes=district_vote.votes
    )

# Candidateを作成するAPI
@router.post("/candidates")
def post_candidate(
        candidate: PostCandidateSchema, 
        db: Session = Depends(get_db)
    ):
    # 受け取ったデータからモデルを作成
    db_model = CandidateModel(
        id=candidate.id,
        name=candidate.name,
        party=candidate.party,
        win_count=candidate.win_count
    )
    # データベースに登録（インサート）
    db.add(db_model)
    # 変更内容を確定
    db.commit()

    return {"message": "Candidate Created Successfully."}

# Candidateを削除するAPI
@router.delete("/candidates/{id}")
def delete_candidate(
        id: int,
        db: Session = Depends(get_db)
    ):
    delete_candidate = db.query(CandidateModel).filter(
        CandidateModel.id==id
    ).one()
    db.delete(delete_candidate)
    db.commit()

    return {"message": "Deleted Candidate Successfully."}