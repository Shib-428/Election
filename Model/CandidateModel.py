from sqlalchemy import Column, Integer, String
from settings import Base

class CandidateModel(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    party = Column(String(100), nullable=False) # 所属政党 無所属は「"無所属"所属」の扱いに。
    # party_id = Column(Integer, ForeignKey("parties.id"), nullable=True) # 所属政党
    win_count = Column(Integer, nullable=False) # 当選回数