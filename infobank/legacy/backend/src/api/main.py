from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from db.database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat, dashboard, evaluation, golden_set, system


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Chat QA Ops API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)
app.include_router(evaluation.router)
app.include_router(dashboard.router)
app.include_router(golden_set.router)
app.include_router(system.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
