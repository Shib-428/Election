from fastapi import Depends, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from Model import DistrictVoteModel
from Schema import PostDistrictVoteSchema
from database import get_db

router = APIRouter()

# データベースからDistrictVote一覧を取得するAPI
@router.get("/district_votes")
def get_district_votes(
        db: Session = Depends(get_db)
    ):
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(DistrictVoteModel).all()

# DistrictVoteを作成するAPI
@router.post("/district_votes")
def post_district_vote(
    district_vote: PostDistrictVoteSchema,
    db: Session = Depends(get_db)
):
    # 受け取ったデータからモデルを作成
    db_model = DistrictVoteModel(
        candidate_id=district_vote.candidate_id,
        prefecture=district_vote.prefecture,
        district=district_vote.district,
        votes=district_vote.votes
    )
    # データベースに登録（インサート）
    db.add(db_model)
    # 変更内容を確定
    db.commit()

    return {"message": "District Vote Created Successfully."}

# DistrictVoteを削除するAPI
@router.delete("/district_votes/{candidate_id}")
def delete_district_vote(
        candidate_id: int,
        db: Session = Depends(get_db)
    ):
    delete_district_vote = db.query(DistrictVoteModel).filter(
        DistrictVoteModel.candidate_id==candidate_id
    ).one()
    if not delete_district_vote:
        raise HTTPException(status_code=404, detail="District Vote not found")
    
    db.delete(delete_district_vote)
    db.commit()

    return {"message": "Deleted District Vote Successfully."}
