from __future__ import annotations

from collections.abc import Iterator

from db.database import get_db
from sqlalchemy.orm import Session


def get_session() -> Iterator[Session]:
    yield from get_db()
