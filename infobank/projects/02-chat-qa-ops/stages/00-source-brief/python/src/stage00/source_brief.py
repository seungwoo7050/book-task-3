from dataclasses import dataclass


REFERENCE_SPINE = (
    "README.md",
    "docs/curriculum/legacy-intent-audit.md",
    "docs/curriculum/project-selection-rationale.md",
    "docs/curriculum/curriculum-map.md",
    "docs/curriculum/reference-spine.md",
)


@dataclass(frozen=True)
class SourceBrief:
    topic: str
    capstone_goal: str
    baseline_version: str
    primary_stack: tuple[str, ...]


def build_source_brief() -> SourceBrief:
    return SourceBrief(
        topic="챗봇 상담 품질 관리",
        capstone_goal="QA Ops 플랫폼 데모 완성",
        baseline_version="capstone/v0-initial-demo",
        primary_stack=("Python 3.12", "FastAPI", "Pydantic", "SQLAlchemy", "React", "PostgreSQL", "Langfuse"),
    )
