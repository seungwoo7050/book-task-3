from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from typing import Any

from core.config import Settings


@dataclass
class TraceEnvelope:
    trace_id: str
    lineage_id: str
    transport: str
    run_label: str
    dataset: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_trace_envelope(
    settings: Settings,
    *,
    run_label: str,
    dataset: str,
    metadata: dict[str, Any] | None = None,
) -> TraceEnvelope:
    transport = "noop"
    if settings.langfuse_enabled and settings.langfuse_host and settings.langfuse_public_key:
        transport = "langfuse-prepared"
    return TraceEnvelope(
        trace_id=str(uuid.uuid4()),
        lineage_id=str(uuid.uuid4()),
        transport=transport,
        run_label=run_label,
        dataset=dataset,
        metadata=metadata or {},
    )
