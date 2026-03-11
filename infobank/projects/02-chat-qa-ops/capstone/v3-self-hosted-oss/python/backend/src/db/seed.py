from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from core.json_utils import dumps_json
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import GoldenSet, KnowledgeDoc

DOC_METADATA_HINTS: dict[str, dict[str, object]] = {
    "plans__basic_plan.md": {
        "aliases": ["베이직", "basic", "초과요금", "기본 데이터"],
        "keywords": ["요금제", "39,000원", "10GB", "음성 200분"],
        "risk": "pricing",
    },
    "plans__premium_plan.md": {
        "aliases": ["프리미엄", "premium", "무제한", "150GB"],
        "keywords": ["59,000원", "속도 제어", "위약금"],
        "risk": "pricing",
    },
    "plans__family_plan.md": {
        "aliases": ["가족결합", "패밀리", "회선 결합", "가족 할인"],
        "keywords": ["최대 4개", "할인율", "대표 회선"],
        "risk": "pricing",
    },
    "plans__data_addon.md": {
        "aliases": ["부가팩", "데이터 부가팩", "추가 데이터"],
        "keywords": ["다음 청구 주기", "월 정액"],
        "risk": "pricing",
    },
    "plans__roaming_pack.md": {
        "aliases": ["로밍패스", "로밍 패스", "사전 신청"],
        "keywords": ["국가별", "기간별", "추가 과금"],
        "risk": "pricing",
    },
    "policies__cancellation_policy.md": {
        "aliases": ["위약금", "약정 해지", "할부금", "잔여 할부금"],
        "keywords": ["약정 기간", "부과", "별도 청구"],
        "risk": "policy",
    },
    "policies__discount_policy.md": {
        "aliases": ["할인 확정", "감면", "면제", "무료 제공"],
        "keywords": ["무조건 불가", "확정 안내 금지", "조건별 상이"],
        "risk": "policy",
    },
    "policies__escalation_policy.md": {
        "aliases": ["민원", "분쟁", "환불 거절", "피해", "전문 부서"],
        "keywords": ["즉시 이관", "상담원 연결", "정책 해석 불명확"],
        "risk": "escalation",
    },
    "policies__privacy_policy.md": {
        "aliases": ["주민번호", "카드번호", "개인정보", "전체 번호"],
        "keywords": ["마스킹", "수집 금지", "민감정보"],
        "risk": "privacy",
    },
    "policies__refund_policy.md": {
        "aliases": ["환불", "환불 접수", "영업일", "3~5일"],
        "keywords": ["본인확인", "은행 처리 일정", "지연"],
        "risk": "policy",
    },
    "procedures__cancellation_flow.md": {
        "aliases": ["해지 절차", "번호이동", "자동 해지", "해지 순서"],
        "keywords": ["본인확인", "해지 접수", "약정 확인"],
        "risk": "procedure",
    },
    "procedures__device_insurance.md": {
        "aliases": ["보험", "보상 청구", "청구 서류", "분실 보상"],
        "keywords": ["구매 증빙", "사고 접수", "가입 기간"],
        "risk": "procedure",
    },
    "procedures__identity_verification.md": {
        "aliases": ["본인인증", "본인확인", "명의변경", "인증 실패"],
        "keywords": ["해지 신청", "환불 신청", "추가 확인 절차"],
        "risk": "procedure",
    },
    "procedures__plan_change.md": {
        "aliases": ["요금제 변경", "변경 절차", "변경 방법"],
        "keywords": ["절차", "신청", "처리 순서"],
        "risk": "procedure",
    },
    "procedures__roaming_activation.md": {
        "aliases": ["로밍 활성화", "출국 전", "데이터 차단", "로밍 신청"],
        "keywords": ["재부팅", "차단 옵션", "적용"],
        "risk": "procedure",
    },
}


def seed_knowledge_base(session: Session, root: Path) -> int:
    inserted = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        doc_id = str(rel).replace("/", "__")
        title = path.stem
        category = rel.parts[0] if len(rel.parts) > 1 else "general"
        content = path.read_text(encoding="utf-8").strip()
        metadata: dict[str, object] = {"source": str(rel)}
        metadata.update(DOC_METADATA_HINTS.get(doc_id, {}))

        existing = session.get(KnowledgeDoc, doc_id)
        if existing is None:
            session.add(
                KnowledgeDoc(
                    id=doc_id,
                    title=title,
                    category=category,
                    content=content,
                    metadata_json=dumps_json(metadata),
                )
            )
            inserted += 1
        else:
            existing.title = title
            existing.category = category
            existing.content = content
            existing.metadata_json = dumps_json(metadata)

    return inserted



def seed_golden_set(session: Session, yaml_path: Path) -> int:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    cases: list[dict[str, Any]] = raw.get("cases", [])
    inserted = 0

    for item in cases:
        case_id = str(item["id"])
        existing = session.get(GoldenSet, case_id)
        payload = {
            "expected_failure_types": item.get("expected_failure_types", []),
            "required_evidence_doc_ids": item.get("required_evidence_doc_ids", []),
        }
        tags = item.get("tags", [])

        if existing is None:
            session.add(
                GoldenSet(
                    id=case_id,
                    category=item.get("category", "general"),
                    user_message=item["user_message"],
                    expected_config=dumps_json(payload),
                    tags=dumps_json(tags),
                )
            )
            inserted += 1
        else:
            existing.category = item.get("category", "general")
            existing.user_message = item["user_message"]
            existing.expected_config = dumps_json(payload)
            existing.tags = dumps_json(tags)

    return inserted



def golden_set_count(session: Session) -> int:
    return len(session.scalars(select(GoldenSet.id)).all())
