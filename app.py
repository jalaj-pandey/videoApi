from fastapi import FastAPI
from tutor_route import router as tutor_router



app = FastAPI()


app.include_router(tutor_router, prefix="/tutor")

@app.get("/")
async def get():
    return {"message": "hiii"}
