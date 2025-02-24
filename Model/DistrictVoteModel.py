from sqlalchemy import Column, Integer, ForeignKey, String
from settings import Base

class DistrictVoteModel(Base):
    __tablename__ = "district_votes"

    candidate_id = Column(Integer, ForeignKey("candidates.id"), primary_key=True)
    prefecture = Column(String(50), nullable=False) # 都道府県名
    district = Column(Integer, nullable=False) # 選挙区
    votes = Column(Integer, nullable=False) # 得票数