from fastapi import FastAPI
from app.api import projects, places
from app.db.database import engine
from app.models.base import Base

app = FastAPI(title="Travel Planner API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(projects.router)
app.include_router(places.router)


@app.get("/")
async def root():
    return {"message": "Travel Planner API is running!"}
