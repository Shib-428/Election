from pydantic import BaseModel

class DistrictVoteCreateSchema(BaseModel):
    candidate_id: int
    prefecture: str
    district: str
    votes: int

""" DistrictVoteSchemaと全く同じなので、それを流用しても処理上は問題ない。 """