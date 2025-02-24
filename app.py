from fastapi import FastAPI, Depends, HTTPException
import uvicorn

from Model import CandidateModel, DistrictVoteModel
from Schema import CandidateDetailsResponseSchema, PostCandidateSchema, PostDistrictVoteSchema
from Query import CandidateQueries
from settings import SessionLocal

from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# データベースからCandidate一覧を取得するAPI
@app.get("/candidates")
def get_candidates(
        db: Session = Depends(get_db)
    ):
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(CandidateModel).all()

@app.get("/candidates/{id}", response_model=CandidateDetailsResponseSchema)
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
@app.post("/candidates")
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
@app.delete("/candidates/{id}")
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

# データベースからDistrictVote一覧を取得するAPI
@app.get("/district_votes")
def get_district_votes(
        db: Session = Depends(get_db)
    ):
    # query関数でモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(DistrictVoteModel).all()

# DistrictVoteを作成するAPI
@app.post("/district_votes")
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
@app.delete("/district_votes/{candidate_id}")
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")