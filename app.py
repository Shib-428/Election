from fastapi import FastAPI
import uvicorn

from Router import candidates_router, district_votes_router


app = FastAPI()

app.include_router(candidates_router, prefix='/candidates', tags=['Candidates'])
app.include_router(district_votes_router, prefix='/district_votes', tags=['DistrictVotes'])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")