from pydantic import BaseModel

class CandidateSchema(BaseModel):
    id: int
    name: str
    party: str
    win_count: int

    class Config:
        from_attributes = True  # SQLAlchemy モデルからPydanticモデルを生成可能にする