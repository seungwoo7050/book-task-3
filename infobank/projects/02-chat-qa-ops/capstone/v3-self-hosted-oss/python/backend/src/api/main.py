from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from core.config import load_settings
from db.database import init_db, session_scope
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.bootstrap import bootstrap_admin_user, bootstrap_sample_assets

from api.routes import (
    auth,
    chat,
    dashboard,
    datasets,
    evaluation,
    golden_set,
    jobs,
    kb_bundles,
    system,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    settings = load_settings()
    with session_scope() as session:
        bootstrap_admin_user(session, settings)
        bootstrap_sample_assets(session, settings)
    yield


app = FastAPI(title="Qualbot Self-Hosted QA Ops API", version="0.3.0", lifespan=lifespan)

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


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(evaluation.router)
app.include_router(dashboard.router)
app.include_router(datasets.router)
app.include_router(kb_bundles.router)
app.include_router(jobs.router)
app.include_router(golden_set.router)
app.include_router(system.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
