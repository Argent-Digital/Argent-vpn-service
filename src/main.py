from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.core_api import router as core_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting Argent vpn service...")

    yield

    print("stopped Argent vpn service")

app = FastAPI(
    title="Argent VPN",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(core_router)

@app.get("/")
async def health_check():
    return {"status": "working", "service": "argent-vpn"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
