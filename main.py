

from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.session import engine
from models.job_model import Base
from routes.job_route import router

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Starting app")
    yield

app=FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


