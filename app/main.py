from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.database import (
    close_mongo_connection,
    connect_to_mongo,
    create_indexes,
)
from app.routers import bookings, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await create_indexes()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="MediTrack Cloud",
    description="Hospital appointment booking API",
    version="0.2.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(health.router)
app.include_router(bookings.router)


@app.get("/")
async def root():
    return {"service": "meditrack-cloud", "version": "0.2.0"}
