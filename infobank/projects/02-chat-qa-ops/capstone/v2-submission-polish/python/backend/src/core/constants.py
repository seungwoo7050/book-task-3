from __future__ import annotations

FAILURE_TYPES = {
    "UNSUPPORTED_CLAIM",
    "CONTRADICTED_BY_SOURCE",
    "MISSING_MANDATORY_STEP",
    "FORBIDDEN_PROMISE",
    "PII_EXPOSURE",
    "RETRIEVAL_MISS",
    "RETRIEVAL_NOISE",
    "ESCALATION_MISS",
    "FORMATTING_CLARITY_ISSUE",
    "TONE_ISSUE",
}

WEIGHTS = {
    "correctness": 0.30,
    "groundedness": 0.25,
    "compliance": 0.20,
    "resolution": 0.15,
    "communication": 0.10,
}

CRITICAL_GRADE = "CRITICAL"
GRADE_BANDS = [
    ("A", 90.0),
    ("B", 75.0),
    ("C", 60.0),
    ("D", 40.0),
    ("F", 0.0),
]
