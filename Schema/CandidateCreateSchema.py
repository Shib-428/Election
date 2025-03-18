from pydantic import BaseModel

class CandidateCreateSchema(BaseModel):
    id: int
    name: str
    party: str
    win_count: int

""" CandidateSchemaと全く同じなので、それを流用しても処理上は問題ない。 """