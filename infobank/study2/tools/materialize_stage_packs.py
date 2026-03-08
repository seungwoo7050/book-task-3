from __future__ import annotations

import json
import shutil
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
V1_REACT = ROOT / "08-capstone-submission" / "v1-regression-hardening" / "react"
CHECKED_DATE = "2026-03-07"

STAGE_META: dict[str, dict[str, object]] = {
    "00-source-brief": {
        "summary": "legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.",
        "stage_question": "이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?",
        "inputs": [
            "루트 `README.md`와 `docs/legacy-intent-audit.md`의 프로젝트 의도",
            "`docs/project-selection-rationale.md`, `docs/curriculum-map.md`, `docs/reference-spine.md`의 커리큘럼 근거",
            "`08-capstone-submission/v0-initial-demo`를 baseline으로 삼는 버전 전략",
        ],
        "outputs": [
            "`python/src/stage00/source_brief.py`의 `SourceBrief` dataclass",
            "reference spine tuple과 baseline version contract",
            "stage-local pytest로 검증되는 stack/sequence snapshot",
        ],
        "success": [
            "주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.",
            "reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.",
            "후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.",
        ],
        "paths": [
            "`python/src/stage00/source_brief.py`",
            "`python/tests/test_source_brief.py`",
        ],
        "concepts": [
            "문서 중심 기획을 코드 계약으로 고정하는 방법",
            "baseline snapshot과 curriculum rationale의 분리",
            "reference spine을 stable navigation으로 유지하는 원칙",
        ],
        "capstone_mapping": [
            "`08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.",
            "이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.",
        ],
        "verification_notes": [
            "테스트는 topic, baseline version, primary stack, reference spine 길이를 고정한다.",
            "runtime을 검증하는 단계는 아니므로 build보다 contract drift 방지가 핵심이다.",
        ],
        "prerequisites": [
            "루트 문서에서 legacy intent와 새 커리큘럼 순서를 읽어야 한다.",
            "capstone이 챗봇 제품이 아니라 QA Ops 플랫폼이라는 점을 먼저 이해해야 한다.",
        ],
        "evidence": [
            "`python/tests/test_source_brief.py`가 baseline version과 stack contract를 검증한다.",
            "생성된 stage README가 `00 -> 08` 순서를 repository-level index로 연결한다.",
        ],
        "uncertainty": "이 단계는 설계 방향을 고정할 뿐, 실제 evaluator나 dashboard가 동작함을 입증하지는 않는다.",
        "decisions": [
            {
                "choice": "source brief를 불변 dataclass와 상수 tuple로 표현했다.",
                "reason": "문장형 README만으로는 이후 stage에서 baseline이나 stack이 쉽게 drift했기 때문이다.",
            },
            {
                "choice": "reference spine을 다섯 문서로 제한했다.",
                "reason": "읽어야 할 문서 수를 최소화해 다른 사람이 repository를 빠르게 이해하도록 만들기 위해서다.",
            },
        ],
        "rejected": [
            "README 서술만 남기고 코드 계약은 만들지 않는 방식",
            "legacy 디렉터리 구조를 그대로 학습 sequence로 간주하는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "stack 설명이 문서마다 조금씩 달라질 위험이 있었다.",
                "cause": "Python 버전과 backend/frontend 주력 기술이 코드가 아니라 서술에만 있었다.",
                "fix": "SourceBrief에 Python 3.12, FastAPI, React, PostgreSQL, Langfuse를 명시하고 테스트로 고정했다.",
                "verify": "`python/tests/test_source_brief.py`가 stack membership와 baseline version을 검증한다.",
            }
        ],
        "strengths": [
            "후속 stage에서 참조할 baseline과 stack이 명확하다.",
            "legacy 의도와 새 curriculum rationale이 같은 파일에서 연결된다.",
        ],
        "weaknesses": [
            "실행 시스템이 아니라 navigation contract라서 체감 기능은 적다.",
            "reference spine의 내용 품질은 별도 문서 관리에 의존한다.",
        ],
        "revisit": [
            "향후 다른 study track이 생기면 source brief schema를 공통 모듈로 승격할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Reference Spine",
                "reference": "study2/docs/reference-spine.md",
                "why": "source brief가 어떤 문서를 canonical source로 삼는지 확인하기 위해 읽었다.",
                "learned": "트랙 전체의 문제 정의와 제출 방향은 소수의 상위 문서에 집중되어 있었다.",
                "effect": "stage00에서는 reference spine을 상수 목록으로 유지하도록 결정했다.",
            },
            {
                "title": "Project Selection Rationale",
                "reference": "study2/docs/project-selection-rationale.md",
                "why": "왜 상담 품질 관리 주제가 최종 capstone인지 확인하기 위해 읽었다.",
                "learned": "이 트랙은 상담 챗봇 기능보다 평가와 운영 툴링에 학습 초점이 있다.",
                "effect": "source brief의 capstone goal을 QA Ops 플랫폼으로 고정했다.",
            },
        ],
    },
    "01-quality-rubric-and-score-contract": {
        "summary": "상담 품질 평가의 점수 계약을 독립적으로 고정해 이후 judge와 dashboard가 같은 숫자 언어를 쓰도록 만드는 단계다.",
        "stage_question": "정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?",
        "inputs": [
            "stage00에서 고정한 QA Ops 문제 정의",
            "상담 품질 축인 correctness, groundedness, compliance, resolution, communication",
            "critical failure가 일반 가중 점수를 덮어써야 한다는 제출 요구",
        ],
        "outputs": [
            "`python/src/stage01/rubric.py`의 weight/grade band/merge contract",
            "critical override를 포함한 deterministic tests",
        ],
        "success": [
            "weight 총합이 1.0으로 유지된다.",
            "critical failure는 어떤 점수보다 우선한다.",
            "grade band가 후속 stage와 capstone에서 재사용 가능하다.",
        ],
        "paths": [
            "`python/src/stage01/rubric.py`",
            "`python/tests/test_rubric.py`",
        ],
        "concepts": [
            "weighted rubric 설계",
            "critical override와 grade band의 분리",
            "judge 출력과 final score merge 계약",
        ],
        "capstone_mapping": [
            "v0~v2 모두 같은 scoring vocabulary를 사용한다.",
            "dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.",
        ],
        "verification_notes": [
            "테스트는 weight sum, critical override, high-score grade band를 검증한다.",
            "이 단계는 LLM judge 품질이 아니라 merge contract 안정성을 검증한다.",
        ],
        "prerequisites": [
            "QA Ops의 목표가 상담 품질을 수치화하고 비교하는 것임을 알아야 한다.",
        ],
        "evidence": [
            "`python/tests/test_rubric.py` 세 케이스가 점수 contract를 고정한다.",
            "critical override는 `CRITICAL` grade와 `0.0` total로 정규화된다.",
        ],
        "uncertainty": "weight 값 자체가 인간 평가자 합의로 교정된 것은 아니다. 이 단계는 calibration보다 contract freeze가 목적이다.",
        "decisions": [
            {
                "choice": "rubric과 grade band를 judge로부터 분리했다.",
                "reason": "judge 구현이 heuristic이든 LLM이든 최종 점수 체계는 동일해야 했기 때문이다.",
            },
            {
                "choice": "critical failure를 별도 branch로 처리했다.",
                "reason": "가중 평균 안에서 critical severity를 표현하면 설명 가능성과 회귀 검증이 약해진다.",
            },
        ],
        "rejected": [
            "judge 프롬프트가 자유롭게 총점을 반환하도록 두는 방식",
            "grade band 없이 raw score만 저장하는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "critical failure가 있어도 평균 점수가 높게 계산될 수 있었다.",
                "cause": "weighted average만 사용하면 severe compliance 위반이 다른 축에 묻힐 수 있다.",
                "fix": "`critical=True`일 때 즉시 `CRITICAL` 결과를 반환하도록 분기했다.",
                "verify": "`test_critical_override_wins`가 100점 입력에서도 `CRITICAL`을 기대한다.",
            }
        ],
        "strengths": [
            "후속 stage에서 judge와 evidence verifier를 독립 개발할 수 있다.",
            "평가 결과를 비교할 때 score drift 원인을 좁히기 쉽다.",
        ],
        "weaknesses": [
            "grade band 임계값은 아직 empirical tuning이 아니다.",
        ],
        "revisit": [
            "실제 golden set 평가를 더 모으면 threshold calibration 근거를 추가할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Quality Rubric Contract",
                "reference": "study2/01-quality-rubric-and-score-contract/python/src/stage01/rubric.py",
                "why": "score 계산 규칙을 가장 작은 형태로 고정하기 위해 확인했다.",
                "learned": "scoring vocabulary를 먼저 얼려두면 후속 실험이 숫자 비교로 귀결된다.",
                "effect": "v1/v2 compare도 동일한 score axes를 공유하게 했다.",
            }
        ],
    },
    "02-domain-fixtures-and-chat-harness": {
        "summary": "seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.",
        "stage_question": "fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?",
        "inputs": [
            "환불, 해지, 본인확인 같은 한국어 상담 도메인 샘플 문서",
            "예상 evidence 문서를 가진 replay 세션 목록",
        ],
        "outputs": [
            "`python/data/knowledge_base/*.md` seeded KB",
            "`python/data/replay_sessions.json` replay fixture",
            "`python/src/stage02/harness.py` deterministic replay runner",
        ],
        "success": [
            "같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.",
            "fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.",
            "후속 golden set과 version compare 입력으로 이어질 수 있다.",
        ],
        "paths": [
            "`python/data/knowledge_base/`",
            "`python/data/replay_sessions.json`",
            "`python/src/stage02/harness.py`",
        ],
        "concepts": [
            "seeded KB 설계",
            "deterministic replay harness",
            "expected evidence document 확인 방식",
        ],
        "capstone_mapping": [
            "v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.",
            "v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.",
        ],
        "verification_notes": [
            "테스트는 seeded KB 파일 집합과 첫 replay의 top-1 문서를 검증한다.",
            "DB나 vector store 없이도 회귀 입력 contract를 설명할 수 있어야 한다.",
        ],
        "prerequisites": [
            "평가기가 답변 품질만 보지 않고 어떤 지식을 인용했는지도 확인해야 한다.",
        ],
        "evidence": [
            "`python/tests/test_harness.py`가 fixture loading과 replay 결과를 검증한다.",
            "fixture 파일은 markdown과 JSON으로 분리되어 사람이 직접 검토하기 쉽다.",
        ],
        "uncertainty": "이 pack의 retrieval은 keyword 수준이다. 실제 capstone의 retrieval 품질을 그대로 대변하지는 않는다.",
        "decisions": [
            {
                "choice": "fixture를 코드 안에 하드코딩하지 않고 파일로 분리했다.",
                "reason": "golden set과 replay는 사람이 diff로 검토할 수 있어야 회귀 원인 분석이 쉽다.",
            },
            {
                "choice": "deterministic harness에는 단순 keyword matching을 사용했다.",
                "reason": "stage 목표가 search quality가 아니라 재현 가능한 입력/출력 contract이기 때문이다.",
            },
        ],
        "rejected": [
            "stage pack에서 바로 Chroma나 live provider를 요구하는 방식",
            "replay transcript를 테스트 파일에만 넣는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "짧은 한국어 질의가 content token만으로는 원하는 문서에 닿지 않을 수 있었다.",
                "cause": "질의어와 문서 본문 단어가 완전히 일치하지 않아 filename 단서가 필요했다.",
                "fix": "검색 점수에 doc_id 매칭도 포함해 fixture 재현성을 확보했다.",
                "verify": "`test_replay_harness_reproduces_expected_docs`가 `refund_policy.md`를 top-1로 요구한다.",
            }
        ],
        "strengths": [
            "fixture와 harness 경계가 분명해 회귀 입력을 버전 관리하기 쉽다.",
            "사람이 읽을 수 있는 KB와 replay transcript를 유지한다.",
        ],
        "weaknesses": [
            "실제 고객 대화처럼 다중 턴 상태를 반영하지는 않는다.",
        ],
        "revisit": [
            "추후 replay fixture를 YAML까지 확장하면 capstone의 richer metadata를 더 잘 반영할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Replay Harness",
                "reference": "study2/08-capstone-submission/v0-initial-demo/python/backend/src/evaluator/replay_harness.py",
                "why": "capstone의 재생 경로를 축소 구현할 때 어떤 계약이 핵심인지 확인하기 위해 읽었다.",
                "learned": "fixture 구조가 안정적이어야 regression과 dashboard 수치가 같은 입력을 공유할 수 있다.",
                "effect": "stage02는 KB와 replay JSON을 별도 파일로 분리했다.",
            }
        ],
    },
    "03-rule-and-guardrail-engine": {
        "summary": "mandatory notice, forbidden promise, PII, escalation 규칙을 deterministic failure code로 환원하는 단계다.",
        "stage_question": "상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?",
        "inputs": [
            "해지/환불/명의변경 시 본인확인이 필요하다는 도메인 규칙",
            "과장 약속, PII 노출, 민원/분쟁 escalation 조건",
        ],
        "outputs": [
            "`python/data/rules.json` rule set",
            "`python/src/stage03/guardrails.py` 룰 엔진",
            "failure type별 pytest",
        ],
        "success": [
            "mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.",
            "LLM 없이도 재현 가능한 deterministic regression이 가능하다.",
            "후속 score merge에서 compliance 축을 해석할 수 있다.",
        ],
        "paths": [
            "`python/data/rules.json`",
            "`python/src/stage03/guardrails.py`",
            "`python/tests/test_guardrails.py`",
        ],
        "concepts": [
            "rule-based guardrail",
            "failure type taxonomy",
            "한국어 상담 시나리오의 escalation 조건",
        ],
        "capstone_mapping": [
            "v0에서 추가한 escalation rule과 MP2 guardrail tests를 축소한 pack이다.",
            "failure codes는 dashboard failures 페이지와 golden set assertion의 공통 언어가 된다.",
        ],
        "verification_notes": [
            "테스트는 네 가지 대표 failure type을 각각 직접 검증한다.",
            "이 단계는 recall보다 설명 가능성과 deterministic behavior를 우선한다.",
        ],
        "prerequisites": [
            "상담 품질 평가가 단순 친절도보다 안전성과 정책 준수를 우선해야 함을 이해해야 한다.",
        ],
        "evidence": [
            "`python/tests/test_guardrails.py`가 네 가지 규칙을 각각 분리 검증한다.",
            "룰은 JSON 파일로 분리되어 정책 변경이 코드 diff 없이도 보인다.",
        ],
        "uncertainty": "동의어와 문맥 변형을 모두 포착하지는 못한다. 이 pack은 rule surface를 설명하기 위한 최소 범위다.",
        "decisions": [
            {
                "choice": "실패 원인을 `MISSING_MANDATORY_STEP`, `UNSUPPORTED_CLAIM`, `PII_EXPOSURE`, `ESCALATION_MISS`로 분리했다.",
                "reason": "dashboard와 golden set이 어떤 축에서 실패했는지 바로 읽어야 하기 때문이다.",
            },
            {
                "choice": "정책 소스는 JSON으로 두고 engine은 단순 membership 검사로 유지했다.",
                "reason": "stage 목표가 regex DSL 확장이 아니라 규칙 종류를 분명히 드러내는 데 있기 때문이다.",
            },
        ],
        "rejected": [
            "stage 단계에서 LLM safety classifier에 의존하는 방식",
            "하나의 generic compliance score만 남기고 failure type을 버리는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "민원 또는 분쟁 표현이 들어와도 상담원 이관 부재가 따로 보이지 않을 수 있었다.",
                "cause": "escalation 규칙을 mandatory notice와 같은 bucket으로 섞으면 원인 분석이 어려웠다.",
                "fix": "escalation 전용 failure type과 trigger term 목록을 분리했다.",
                "verify": "`test_escalation_rule`이 `ESCALATION_MISS`를 직접 기대한다.",
            }
        ],
        "strengths": [
            "실패 이유가 명확해 품질 논의를 human-review와 연결하기 쉽다.",
            "golden regression에서 재현 가능한 failure taxonomy를 제공한다.",
        ],
        "weaknesses": [
            "rule coverage 확장은 수동 유지보수 비용이 든다.",
        ],
        "revisit": [
            "실제 상담 로그를 더 확보하면 synonym dictionary를 늘리거나 regex DSL을 도입할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Mandatory Notice And Escalation Rules",
                "reference": "study2/08-capstone-submission/v0-initial-demo/python/backend/rules/mandatory_notices.yaml",
                "why": "v0에 반영한 한국어 안전 규칙을 stage pack으로 축소 재현하기 위해 읽었다.",
                "learned": "mandatory notice와 escalation은 둘 다 compliance이지만 실패 원인이 달라 별도 분리가 필요했다.",
                "effect": "stage03에서는 escalation miss를 전용 failure code로 유지했다.",
            }
        ],
    },
    "04-claim-and-evidence-pipeline": {
        "summary": "답변에서 claim을 분리하고 각 claim에 retrieval trace와 verdict trace를 남기는 groundedness 검증 단계를 다룬다.",
        "stage_question": "답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?",
        "inputs": [
            "assistant response text",
            "seeded knowledge base 또는 doc_id -> content 매핑",
        ],
        "outputs": [
            "claim list",
            "claim별 `support` 또는 `not_found` verdict",
            "retrieval trace와 evidence_doc_ids",
        ],
        "success": [
            "각 claim 결과에 retrieval query와 matched docs가 남는다.",
            "근거가 없는 문장도 `not_found`로 기록되어 silent drop이 없다.",
            "후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.",
        ],
        "paths": [
            "`python/src/stage04/pipeline.py`",
            "`python/tests/test_pipeline.py`",
        ],
        "concepts": [
            "claim extraction",
            "retrieval trace",
            "verdict trace와 evidence document linkage",
        ],
        "capstone_mapping": [
            "v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 축소판이다.",
            "session review 페이지가 보여주는 provenance 데이터의 핵심 구조를 먼저 설명한다.",
        ],
        "verification_notes": [
            "테스트는 첫 claim이 `support` verdict와 예상 doc trace를 남기는지 확인한다.",
            "silent success보다 trace completeness를 더 중요하게 본다.",
        ],
        "prerequisites": [
            "groundedness가 단순 yes/no가 아니라 문장 단위 provenance여야 한다는 점을 이해해야 한다.",
        ],
        "evidence": [
            "`python/tests/test_pipeline.py`가 retrieval trace 보존을 직접 검증한다.",
            "pipeline은 vector DB 없이도 trace schema를 설명 가능하게 유지한다.",
        ],
        "uncertainty": "claim segmentation은 단순 문장 분리라 실제 복합 문장이나 함축 표현을 충분히 다루지 못한다.",
        "decisions": [
            {
                "choice": "claim extraction과 evidence verification을 별도 함수로 분리했다.",
                "reason": "trace가 어느 단계에서 생성되는지 분리해야 디버깅과 교체가 쉽다.",
            },
            {
                "choice": "근거가 없는 claim도 결과에서 제거하지 않고 `not_found`로 남긴다.",
                "reason": "평가 파이프라인에서 빠진 claim은 향후 missing evidence failure로 연결되어야 하기 때문이다.",
            },
        ],
        "rejected": [
            "답변 전체를 하나의 groundedness score로만 압축하는 방식",
            "retrieval trace 없이 evidence doc id만 남기는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "근거가 없는 claim이 결과 구조에서 사라지면 왜 groundedness가 낮은지 설명하기 어려웠다.",
                "cause": "matched docs가 없는 claim을 trace 없이 버리면 failure 분석이 불가능하다.",
                "fix": "`not_found` verdict와 빈 docs list를 포함한 claim result를 항상 반환하도록 했다.",
                "verify": "테스트와 구현에서 모든 claim이 결과 리스트에 유지된다.",
            }
        ],
        "strengths": [
            "session review에서 사람이 읽을 provenance data를 남길 수 있다.",
            "retrieval 성능 문제와 answer composition 문제를 분리해서 볼 수 있다.",
        ],
        "weaknesses": [
            "confidence score나 contradiction depth는 아직 없다.",
        ],
        "revisit": [
            "후속 실험에서 domain classification과 reranking을 trace schema에 더 붙일 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Evidence Verifier Trace Shape",
                "reference": "study2/08-capstone-submission/v1-regression-hardening/python/backend/src/evaluator/evidence_verifier.py",
                "why": "capstone에서 어떤 trace 항목이 실제로 필요한지 확인하기 위해 읽었다.",
                "learned": "retrieval query, returned docs, verdict, evidence ids를 한 덩어리로 봐야 groundedness를 설명할 수 있다.",
                "effect": "stage04는 retrieval trace와 verdict trace를 최소 schema로 유지했다.",
            }
        ],
    },
    "05-judge-and-score-merge": {
        "summary": "judge 결과와 rubric merge를 분리해 품질 판단과 점수 계산의 경계를 명확히 만드는 단계다.",
        "stage_question": "응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?",
        "inputs": [
            "user message",
            "assistant response",
            "failure types",
            "groundedness와 compliance 서브스코어",
        ],
        "outputs": [
            "judge result dictionary",
            "weighted final score",
        ],
        "success": [
            "judge와 scorer가 별도 함수 계약을 가진다.",
            "failure types는 판단 결과와 최종 score 계산 모두에 반영된다.",
            "live provider가 없어도 deterministic 테스트가 가능하다.",
        ],
        "paths": [
            "`python/src/stage05/judge.py`",
            "`python/tests/test_judge.py`",
        ],
        "concepts": [
            "judge output schema",
            "heuristic scoring",
            "quality axes merge",
        ],
        "capstone_mapping": [
            "v1의 LLM judge trace와 stage01 rubric contract 사이를 잇는 중간 단계다.",
            "추후 provider가 바뀌어도 merge contract는 유지된다는 점을 보여준다.",
        ],
        "verification_notes": [
            "테스트는 failure가 없는 응답의 total score와 empty failure types를 검증한다.",
            "이 stage는 live provider 품질보다 interface boundary를 보는 것이 목적이다.",
        ],
        "prerequisites": [
            "stage01의 weighted rubric과 stage03의 failure taxonomy를 알고 있어야 한다.",
        ],
        "evidence": [
            "`python/tests/test_judge.py`가 judge+merge 조합 결과를 검증한다.",
        ],
        "uncertainty": "heuristic judge는 실제 상담 품질의 뉘앙스를 충분히 반영하지 못한다. stage 목적은 interface freeze다.",
        "decisions": [
            {
                "choice": "judge는 subscore와 failure types를 만들고, merge는 final score만 계산하게 분리했다.",
                "reason": "LLM judge를 도입하더라도 final scoring contract는 별도로 검증 가능해야 하기 때문이다.",
            },
            {
                "choice": "stage pack에서는 heuristic judge를 유지했다.",
                "reason": "외부 모델 의존성 없이도 score merge 구조를 설명하고 테스트할 수 있어야 한다.",
            },
        ],
        "rejected": [
            "judge가 총점까지 직접 반환하는 monolithic evaluator",
            "groundedness/compliance를 judge 내부 추정치로만 숨기는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "짧은 응답도 무조건 높은 resolution 점수를 받을 수 있었다.",
                "cause": "응답 길이와 안내성 표현을 별도 기준으로 보지 않으면 resolution과 communication이 구분되지 않는다.",
                "fix": "response length와 안내/확인 표현 유무로 resolution, communication을 분리했다.",
                "verify": "`judge_response` 구현이 길이와 표현 여부를 다른 축으로 평가한다.",
            }
        ],
        "strengths": [
            "judge 모델을 바꾸어도 merge 검증은 그대로 유지된다.",
            "failure taxonomy와 score axes의 연결이 명확하다.",
        ],
        "weaknesses": [
            "heuristic 기준이 실제 상담 품질 평가자 합의와 일치한다고 보장할 수 없다.",
        ],
        "revisit": [
            "향후 live judge 출력과 heuristic judge 출력을 같은 schema로 비교하는 회귀 실험을 추가할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "LLM Judge Boundary",
                "reference": "study2/08-capstone-submission/v1-regression-hardening/python/backend/src/evaluator/llm_judge.py",
                "why": "stage05가 무엇을 분리해서 보여줘야 하는지 확인하기 위해 읽었다.",
                "learned": "judge trace와 final score merge는 결합되지만 동일 책임은 아니다.",
                "effect": "stage05는 판단과 계산을 분리한 최소 함수를 유지한다.",
            }
        ],
    },
    "06-golden-set-and-regression": {
        "summary": "golden case, assertion, replay summary, compare manifest를 묶어 baseline과 candidate를 같은 데이터셋 위에서 비교하는 단계다.",
        "stage_question": "개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?",
        "inputs": [
            "required evidence doc ids를 가진 golden case",
            "baseline/candidate/dataset을 지정하는 compare manifest",
        ],
        "outputs": [
            "pass/fail assertion 결과",
            "reason code 기반 regression 설명",
            "compare input manifest",
        ],
        "success": [
            "golden case는 required evidence 문서를 명시한다.",
            "assertion 실패는 reason code로 설명된다.",
            "baseline과 candidate label을 manifest 파일로 고정한다.",
        ],
        "paths": [
            "`python/data/golden_cases.json`",
            "`python/data/compare_manifest.json`",
            "`python/src/stage06/regression.py`",
        ],
        "concepts": [
            "golden set assertion",
            "reason code 기반 regression",
            "version compare input manifest",
        ],
        "capstone_mapping": [
            "v1 compare와 v2 improvement report의 최소 구조를 stage 단위로 축소한 것이다.",
            "evidence miss 감소를 수치로 논증하려면 manifest와 assertion이 함께 있어야 한다.",
        ],
        "verification_notes": [
            "테스트는 golden assertion success와 manifest labels를 함께 검증한다.",
            "stage 범위는 데이터셋 계약까지이며 dashboard 저장소는 포함하지 않는다.",
        ],
        "prerequisites": [
            "stage02 fixture/replay, stage04 evidence doc contract를 이해해야 한다.",
        ],
        "evidence": [
            "`python/tests/test_regression.py`가 golden assertion과 compare manifest를 확인한다.",
        ],
        "uncertainty": "이 pack은 sample-size가 작아 통계적 의미를 주장하기보다 compare 구조를 설명하는 데 초점이 있다.",
        "decisions": [
            {
                "choice": "golden cases와 compare manifest를 별도 JSON 파일로 분리했다.",
                "reason": "데이터셋 내용과 비교 대상 메타데이터가 서로 다른 변경 주기를 가지기 때문이다.",
            },
            {
                "choice": "assertion 실패는 `MISSING_REQUIRED_EVIDENCE_DOC` 같은 reason code를 사용한다.",
                "reason": "v2의 개선 효과를 failure type 감소로 직접 비교하기 위해서다.",
            },
        ],
        "rejected": [
            "비교 대상을 테스트 코드에 하드코딩하는 방식",
            "pass/fail만 남기고 failure reason을 버리는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "baseline과 candidate가 어떤 run label인지 문서만 봐서는 혼동될 수 있었다.",
                "cause": "compare input이 코드 호출부에만 숨어 있으면 proof artifact와 추적이 끊긴다.",
                "fix": "`compare_manifest.json`에 baseline, candidate, dataset을 분리 저장했다.",
                "verify": "`test_golden_assertion_and_compare_manifest`가 `v1.0`, `v1.1`, `golden-set` 값을 검증한다.",
            }
        ],
        "strengths": [
            "비교 대상과 데이터셋 범위가 명시적이다.",
            "failure type 감소를 개선의 근거로 삼기 쉽다.",
        ],
        "weaknesses": [
            "실제 capstone처럼 run registry나 dashboard와 연결되지는 않는다.",
        ],
        "revisit": [
            "향후 precision/recall 같은 richer assertion 메트릭을 추가할 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Improvement Manifest",
                "reference": "study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json",
                "why": "stage06이 최종 capstone 증빙과 어떤 관계를 가지는지 확인하기 위해 읽었다.",
                "learned": "비교 실험은 숫자 자체보다 같은 입력과 레이블을 공유하는 manifest가 중요하다.",
                "effect": "stage06은 baseline/candidate/dataset을 별도 manifest로 유지한다.",
            }
        ],
    },
    "07-monitoring-dashboard-and-review-console": {
        "summary": "overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.",
        "stage_question": "평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?",
        "inputs": [
            "overview/failure/session/version compare snapshot payload",
            "React dashboard pages와 mocked tests",
        ],
        "outputs": [
            "FastAPI snapshot endpoints",
            "React pages for overview, failures, session review, eval runner",
            "version compare UI and mocked integration tests",
        ],
        "success": [
            "운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.",
            "backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.",
            "run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.",
        ],
        "paths": [
            "`python/src/stage07/app.py`",
            "`python/tests/test_api.py`",
            "`react/src/pages/Overview.tsx`",
            "`react/src/pages/SessionReview.tsx`",
        ],
        "concepts": [
            "snapshot API",
            "dashboard information architecture",
            "session review trace surfacing",
            "baseline/candidate version compare",
        ],
        "capstone_mapping": [
            "v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.",
            "v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.",
        ],
        "verification_notes": [
            "Python pack은 snapshot endpoint contract를 테스트한다.",
            "React pack은 mocked Vitest로 overview, failures, session review, eval runner, compare UI를 검증한다.",
        ],
        "prerequisites": [
            "run label, retrieval version, failure taxonomy, score contract를 이미 알고 있어야 콘솔이 읽힌다.",
        ],
        "evidence": [
            "`python/tests/test_api.py`가 overview, failures, conversation detail, golden run, version compare endpoint를 검증한다.",
            "`react` pack은 copied mocked tests로 주요 화면을 검증한다.",
        ],
        "uncertainty": "stage07은 persistent storage 없이 snapshot payload를 보여주므로 실제 운영 데이터 규모나 latency를 검증하지는 않는다.",
        "decisions": [
            {
                "choice": "UI를 새로 설계하지 않고 v1 dashboard slice를 stage pack으로 복제했다.",
                "reason": "stage 목표가 시각적 재창작이 아니라 운영 콘솔의 정보 구조를 분리 학습하는 데 있기 때문이다.",
            },
            {
                "choice": "backend는 snapshot payload를 반환하는 FastAPI app으로 축소했다.",
                "reason": "DB persistence 없이도 화면이 어떤 계약을 기대하는지 설명할 수 있어야 하기 때문이다.",
            },
        ],
        "rejected": [
            "frontend만 남기고 API contract는 문서로만 설명하는 방식",
            "stage07에서도 full DB-backed dashboard를 그대로 끌어오는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "문서 생성이 너무 얇으면 stage07이 단순 UI 복사본처럼 보였다.",
                "cause": "overview, failures, session review, compare가 각각 어떤 운영 질문에 답하는지 서술이 없었다.",
                "fix": "problem/docs/notion에 화면별 책임과 trace surface를 명시적으로 추가했다.",
                "verify": "재생성된 stage07 문서가 API/React pack과 version compare 목적을 구분해 설명한다.",
            }
        ],
        "strengths": [
            "운영 콘솔이 어떤 질문에 답해야 하는지 stage 수준에서 분리 학습할 수 있다.",
            "backend/frontend payload shape를 함께 검증한다.",
        ],
        "weaknesses": [
            "real API wiring과 persistent storage는 capstone 버전에서만 완전하다.",
        ],
        "revisit": [
            "향후 screenshot 기반 docs나 storybook-style examples를 추가하면 공개 저장소 이해도가 더 높아질 수 있다.",
        ],
        "knowledge": [
            {
                "title": "Dashboard Compare Contract",
                "reference": "study2/08-capstone-submission/v1-regression-hardening/react/src/pages/Overview.tsx",
                "why": "운영 콘솔이 compare delta를 어떻게 읽히게 하는지 확인하기 위해 읽었다.",
                "learned": "score delta뿐 아니라 pass/fail/critical delta와 failure breakdown이 함께 보여야 개선 효과를 설득할 수 있다.",
                "effect": "stage07 docs와 snapshot payload에도 compare details를 포함했다.",
            }
        ],
    },
    "08-capstone-submission": {
        "summary": "v0 runnable snapshot, v1 hardening, v2 improvement proof를 묶은 최종 QA Ops capstone 아카이브다.",
        "stage_question": "상담 품질 관리 플랫폼을 runnable demo, regression hardening, improvement proof까지 포함한 제출물로 어떻게 마감할 것인가?",
        "inputs": [
            "00~07 stage에서 분리해 고정한 source brief, rubric, fixtures, guardrails, traces, compare contract, dashboard shape",
            "v0 baseline runnable snapshot",
            "v1 provider chain and lineage hardening",
            "v2 retrieval improvement experiment",
        ],
        "outputs": [
            "`v0-initial-demo`, `v1-regression-hardening`, `v2-submission-polish` snapshot directories",
            "proof artifacts under `v2-submission-polish/docs/demo/proof-artifacts`",
            "release-readiness documents with verification commands and compare summary",
        ],
        "success": [
            "v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.",
            "compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.",
            "fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.",
        ],
        "paths": [
            "`08-capstone-submission/README.md`",
            "`08-capstone-submission/docs/release-readiness.md`",
            "`08-capstone-submission/v0-initial-demo`",
            "`08-capstone-submission/v1-regression-hardening`",
            "`08-capstone-submission/v2-submission-polish`",
        ],
        "concepts": [
            "immutable version snapshots",
            "provider fallback chain",
            "trace-rich evaluation pipeline",
            "run-level version compare",
            "RAG improvement proof",
        ],
        "capstone_mapping": [
            "이 항목 자체가 최종 제출물이다.",
            "tracked docs는 stable index 역할을 하고, notion은 process-heavy technical notebook 역할을 한다.",
        ],
        "verification_notes": [
            "`v0`, `v1`, `v2` 모두 `UV_PYTHON=python3.12 make gate-all`을 통과시켰다.",
            "`v1`, `v2`에서 `make smoke-postgres`를 통과시켰다.",
            "baseline/candidate compare 결과는 `avg_score 84.06 -> 87.76`, `critical 2 -> 0`, `pass 16 -> 19`, `fail 14 -> 11`이다.",
        ],
        "prerequisites": [
            "Python 3.12 환경과 `uv`, `pnpm`, Docker가 있으면 검증을 재현하기 쉽다.",
            "live Upstage/OpenAI/Langfuse 자격증명이 없어도 mock/no-op 경로로 테스트는 가능하다.",
        ],
        "evidence": [
            "`docs/release-readiness.md`와 `study2/release-readiness.md`에 실제 실행 명령과 결과가 정리되어 있다.",
            "`v2-submission-polish/docs/demo/proof-artifacts` 아래에 compare/output artifacts가 저장되어 있다.",
        ],
        "uncertainty": "live Upstage/OpenAI/Langfuse 호출은 이 저장소에서 기본 검증 경로에 포함하지 않았다. 현재 증빙은 mock/no-op와 local fallback을 기준으로 한다.",
        "decisions": [
            {
                "choice": "버전은 폴더 단위 snapshot으로 유지했다.",
                "reason": "v0, v1, v2의 역할과 검증 결과를 분리해 학습 기록과 제출 증빙을 동시에 보존하기 위해서다.",
            },
            {
                "choice": "v1은 안정화, v2는 retrieval improvement proof에 집중하도록 역할을 고정했다.",
                "reason": "한 버전에서 너무 많은 축을 동시에 바꾸면 compare 결과 해석이 어려워진다.",
            },
            {
                "choice": "provider chain은 Upstage Solar 우선, OpenAI 보조, Ollama fallback 구조로 유지했다.",
                "reason": "한국어 성능, 상용 API 호환성, 로컬 fallback을 함께 확보하려는 요구와 맞기 때문이다.",
            },
        ],
        "rejected": [
            "v0 폴더를 직접 계속 수정하는 in-place versioning",
            "개선 실험과 안정화 작업을 한 버전에 동시에 몰아넣는 방식",
            "live provider 검증 없이는 전체 저장소를 설명할 수 없다고 보는 방식",
        ],
        "debug_cases": [
            {
                "symptom": "`make gate-all`이 기본 Python 3.14 환경에서 `chromadb` import 문제로 깨졌다.",
                "cause": "실사용 dependency 조합이 Python 3.12를 전제로 안정화되어 있었기 때문이다.",
                "fix": "각 Python 구현에 `.python-version`과 `requires-python >=3.12,<3.13` 계약을 추가하고 검증 명령도 `UV_PYTHON=python3.12`로 고정했다.",
                "verify": "v0, v1, v2 모두 `UV_PYTHON=python3.12 make gate-all`을 통과했다.",
            },
            {
                "symptom": "baseline 실패 원인 중 `MISSING_REQUIRED_EVIDENCE_DOC` 비중이 높았다.",
                "cause": "retrieval이 도메인/리스크 힌트를 충분히 사용하지 못해 답변이 필요한 문서를 놓쳤다.",
                "fix": "v2에 alias, category hint, risk-aware doc preference, retrieval-conditioned answer composer를 추가했다.",
                "verify": "v2 compare 결과에서 fail count가 14에서 11로 줄고 critical count가 2에서 0으로 감소했다.",
            },
        ],
        "strengths": [
            "구현, 테스트, proof artifact, public docs가 서로 연결되어 있다.",
            "버전별 학습 목적과 변경 범위가 명확하다.",
        ],
        "weaknesses": [
            "external provider와 observability stack은 mock/no-op 검증이 주 경로다.",
            "notion 문서는 local-only라 공개 저장소 이해는 tracked docs에 의존한다.",
        ],
        "revisit": [
            "실제 Upstage/OpenAI/Langfuse 자격증명이 준비되면 live smoke run 문서를 별도 부록으로 추가할 수 있다.",
            "dashboard screenshots를 자동 재생성하는 스크립트를 붙이면 proof artifact 갱신이 더 쉬워진다.",
        ],
        "knowledge": [
            {
                "title": "Release Readiness",
                "reference": "study2/08-capstone-submission/docs/release-readiness.md",
                "why": "공개 저장소 기준으로 어떤 검증이 실제로 완료되었는지 정리하기 위해 읽었다.",
                "learned": "최종본은 단순히 코드가 있는 상태가 아니라, 실제 실행 명령과 결과가 연결된 상태여야 한다.",
                "effect": "capstone docs와 notion에 검증 명령과 결과를 명시적으로 넣었다.",
            },
            {
                "title": "Improvement Proof Artifacts",
                "reference": "study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json",
                "why": "v2 개선 실험을 문서가 아니라 데이터로 설명하기 위해 확인했다.",
                "learned": "improvement claim은 compare labels, dataset, delta metrics를 함께 남겨야 신뢰할 수 있다.",
                "effect": "capstone notebook에서 숫자와 artifact path를 같이 기록하도록 했다.",
            },
        ],
    },
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_debug_cases(cases: list[dict[str, str]]) -> str:
    sections = []
    for index, case in enumerate(cases, start=1):
        sections.append(
            "\n".join(
                [
                    f"### Case {index}",
                    f"- symptom: {case['symptom']}",
                    f"- cause: {case['cause']}",
                    f"- fix: {case['fix']}",
                    f"- verification: {case['verify']}",
                ]
            )
        )
    return "\n\n".join(sections)


def render_decisions(decisions: list[dict[str, str]]) -> str:
    return "\n".join(f"- {decision['choice']} 이유: {decision['reason']}" for decision in decisions)


def render_knowledge(entries: list[dict[str, str]]) -> str:
    sections = []
    for entry in entries:
        sections.append(
            "\n".join(
                [
                    f"## {entry['title']}",
                    f"- title: {entry['title']}",
                    f"- reference: {entry['reference']}",
                    f"- checked date: {CHECKED_DATE}",
                    f"- why consulted: {entry['why']}",
                    f"- learned: {entry['learned']}",
                    f"- effect on project: {entry['effect']}",
                ]
            )
        )
    return "\n\n".join(sections)


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("node_modules", "dist", ".vite"))


def stage_root(name: str) -> Path:
    return ROOT / name


def write_common_docs(base: Path, title: str, summary: str, commands: list[str], implemented: list[str], staged: list[str]) -> None:
    meta = STAGE_META[base.name]
    summary = dedent(summary).strip()
    command_items = [f"`{command}`" for command in commands]
    readme = (
        f"# {title}\n\n"
        f"{summary}\n\n"
        "## Stage Question\n\n"
        f"{meta['stage_question']}\n\n"
        "## Current Implementation\n\n"
        f"- 구현됨: {', '.join(implemented)}\n"
        f"- staged/known gap: {', '.join(staged) if staged else '없음'}\n"
        "- problem/은 원문 범위와 stage goal을 설명한다.\n"
        "- docs/는 이 stage에서 유지할 개념과 검증 포인트를 요약한다.\n\n"
        "## Key Paths\n\n"
        f"{bullet_list(meta['paths'])}\n\n"
        "## Commands\n\n"
        f"{bullet_list(command_items)}"
    )
    docs = (
        f"# {title} Docs\n\n"
        f"{meta['summary']}\n\n"
        "## Concept Focus\n\n"
        f"{bullet_list(meta['concepts'])}\n\n"
        "## Capstone Mapping\n\n"
        f"{bullet_list(meta['capstone_mapping'])}\n\n"
        "## Implementation Snapshot\n\n"
        f"- 구현됨: {', '.join(implemented)}\n"
        f"- staged/known gap: {', '.join(staged) if staged else '없음'}\n\n"
        "## Verification\n\n"
        f"{bullet_list(command_items)}\n\n"
        "## Notes\n\n"
        f"{bullet_list(meta['verification_notes'])}"
    )
    problem = (
        f"# {title} Problem\n\n"
        f"{meta['summary']}\n\n"
        "## Stage Question\n\n"
        f"{meta['stage_question']}\n\n"
        "## Inputs\n\n"
        f"{bullet_list(meta['inputs'])}\n\n"
        "## Required Output\n\n"
        f"{bullet_list(meta['outputs'])}\n\n"
        "## Success Criteria\n\n"
        f"{bullet_list(meta['success'])}\n\n"
        "## Actual Status\n\n"
        "- implementation directory가 생성되어 있음\n"
        "- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨\n"
        f"- 검증 명령: {', '.join(command_items)}"
    )
    write(base / "README.md", readme)
    write(base / "docs" / "README.md", docs)
    write(base / "problem" / "README.md", problem)


def write_python_pack(base: Path, package: str, readme: str, pyproject: str, files: dict[str, str]) -> None:
    py_base = base / "python"
    write(py_base / "README.md", readme)
    write(py_base / "pyproject.toml", pyproject)
    write(py_base / ".python-version", "3.12.6")
    write(
        py_base / "tests" / "conftest.py",
        """
        import sys
        from pathlib import Path


        SRC = Path(__file__).resolve().parents[1] / "src"
        if str(SRC) not in sys.path:
            sys.path.insert(0, str(SRC))
        """,
    )
    write(py_base / "src" / package / "__init__.py", "")
    for rel_path, content in files.items():
        write(py_base / rel_path, content)


def materialize_stage_00() -> None:
    base = stage_root("00-source-brief")
    write_common_docs(
        base,
        "Stage 00 Source Brief",
        "문제 정의, reference spine, scope contract를 코드 객체로 정리한 source brief pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["reference source manifest", "project selection rationale snapshot"],
        ["capstone runtime 없음"],
    )
    write_python_pack(
        base,
        "stage00",
        """
        # Stage 00 Python

        source brief를 코드 객체로 유지한다. 구현 범위는 reference, gap, sequence contract 정리까지다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: 없음
        """,
        """
        [project]
        name = "study2-stage00"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "src/stage00/source_brief.py": """
            from dataclasses import dataclass


            REFERENCE_SPINE = (
                "README.md",
                "docs/legacy-intent-audit.md",
                "docs/project-selection-rationale.md",
                "docs/curriculum-map.md",
                "docs/reference-spine.md",
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
                    baseline_version="08/v0-initial-demo",
                    primary_stack=("Python 3.12", "FastAPI", "Pydantic", "SQLAlchemy", "React", "PostgreSQL", "Langfuse"),
                )
            """,
            "tests/test_source_brief.py": """
            from stage00.source_brief import REFERENCE_SPINE, build_source_brief


            def test_source_brief_contract():
                brief = build_source_brief()
                assert brief.topic == "챗봇 상담 품질 관리"
                assert brief.baseline_version == "08/v0-initial-demo"
                assert "FastAPI" in brief.primary_stack
                assert len(REFERENCE_SPINE) == 5
            """,
        },
    )


def materialize_stage_01() -> None:
    base = stage_root("01-quality-rubric-and-score-contract")
    write_common_docs(
        base,
        "Stage 01 Quality Rubric",
        "weighted score, grade band, critical override를 독립 패키지로 분리한 rubric contract pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["weighted rubric", "critical override score contract"],
        ["LLM judge 없음"],
    )
    write_python_pack(
        base,
        "stage01",
        """
        # Stage 01 Python

        score contract를 독립 테스트로 고정한다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: 실시간 evaluator 연결 없음
        """,
        """
        [project]
        name = "study2-stage01"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "src/stage01/rubric.py": """
            WEIGHTS = {
                "correctness": 0.30,
                "groundedness": 0.25,
                "compliance": 0.20,
                "resolution": 0.15,
                "communication": 0.10,
            }
            GRADE_BANDS = (("A", 90), ("B", 75), ("C", 60), ("D", 40))


            def to_grade(total: float) -> str:
                for grade, minimum in GRADE_BANDS:
                    if total >= minimum:
                        return grade
                return "F"


            def merge_score(*, correctness: float, groundedness: float, compliance: float, resolution: float, communication: float, critical: bool) -> dict[str, object]:
                if critical:
                    return {"total": 0.0, "grade": "CRITICAL"}
                total = (
                    correctness * WEIGHTS["correctness"]
                    + groundedness * WEIGHTS["groundedness"]
                    + compliance * WEIGHTS["compliance"]
                    + resolution * WEIGHTS["resolution"]
                    + communication * WEIGHTS["communication"]
                )
                total = round(total, 2)
                return {"total": total, "grade": to_grade(total)}
            """,
            "tests/test_rubric.py": """
            from stage01.rubric import WEIGHTS, merge_score


            def test_weights_sum_to_one():
                assert round(sum(WEIGHTS.values()), 5) == 1.0


            def test_critical_override_wins():
                result = merge_score(correctness=100, groundedness=100, compliance=100, resolution=100, communication=100, critical=True)
                assert result == {"total": 0.0, "grade": "CRITICAL"}


            def test_grade_band_contract():
                result = merge_score(correctness=90, groundedness=90, compliance=90, resolution=90, communication=90, critical=False)
                assert result["grade"] == "A"
            """,
        },
    )


def materialize_stage_02() -> None:
    base = stage_root("02-domain-fixtures-and-chat-harness")
    write_common_docs(
        base,
        "Stage 02 Fixtures And Harness",
        "seeded KB, sample conversations, replay harness를 작은 deterministic harness로 재현한 stage pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["seeded KB loader", "deterministic replay harness"],
        ["database 없음"],
    )
    write_python_pack(
        base,
        "stage02",
        """
        # Stage 02 Python

        fixture와 harness만 따로 검증하는 소형 구현이다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: 실제 DB persistence 없음
        """,
        """
        [project]
        name = "study2-stage02"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "data/knowledge_base/cancellation_policy.md": "약정 가입자는 해지 시 위약금이 부과될 수 있습니다.",
            "data/knowledge_base/identity_verification.md": "해지 신청과 환불 신청에는 본인확인이 필수입니다.",
            "data/knowledge_base/refund_policy.md": "환불은 본인확인 후 접수되며 영업일 기준 3~5일이 소요될 수 있습니다.",
            "data/replay_sessions.json": json.dumps(
                {
                    "sessions": [
                        {"user_message": "환불은 몇일 걸려요?", "expected_doc": "refund_policy.md"},
                        {"user_message": "해지 신청은 본인확인 없이 가능해요?", "expected_doc": "identity_verification.md"},
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            "src/stage02/harness.py": """
            import json
            from pathlib import Path


            def seed_knowledge_base(root: Path) -> dict[str, str]:
                return {path.name: path.read_text(encoding="utf-8").strip() for path in sorted(root.glob('*.md'))}


            def retrieve(query: str, kb: dict[str, str]) -> list[str]:
                query_terms = {token for token in query.split() if token}
                scored = []
                for doc_id, content in kb.items():
                    score = sum(1 for term in query_terms if term in content or term in doc_id)
                    if score:
                        scored.append((score, doc_id))
                scored.sort(reverse=True)
                return [doc_id for _, doc_id in scored] or list(kb)[:1]


            def run_replay(path: Path, kb_root: Path) -> dict[str, object]:
                kb = seed_knowledge_base(kb_root)
                replay = json.loads(path.read_text(encoding='utf-8'))
                items = []
                for session in replay['sessions']:
                    docs = retrieve(session['user_message'], kb)
                    items.append({'user_message': session['user_message'], 'retrieved_doc_ids': docs})
                return {'session_count': len(items), 'items': items}
            """,
            "tests/test_harness.py": """
            from pathlib import Path

            from stage02.harness import run_replay, seed_knowledge_base


            def test_seeded_kb_reproducible():
                kb = seed_knowledge_base(Path('data/knowledge_base'))
                assert set(kb) == {'cancellation_policy.md', 'identity_verification.md', 'refund_policy.md'}


            def test_replay_harness_reproduces_expected_docs():
                result = run_replay(Path('data/replay_sessions.json'), Path('data/knowledge_base'))
                assert result['session_count'] == 2
                assert result['items'][0]['retrieved_doc_ids'][0] == 'refund_policy.md'
            """,
        },
    )


def materialize_stage_03() -> None:
    base = stage_root("03-rule-and-guardrail-engine")
    write_common_docs(
        base,
        "Stage 03 Guardrails",
        "mandatory notice, forbidden promise, PII, escalation rule을 독립 룰 엔진으로 분리한 stage pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["rule matcher", "deterministic guardrail tests"],
        ["YAML loader 대신 JSON 사용"],
    )
    rules = {
        "mandatory_notice_terms": ["본인확인", "상담원", "전문 부서"],
        "forbidden_promises": ["무조건", "100%", "반드시"],
        "pii_patterns": ["주민번호", "카드번호", "990101-1234567"],
        "escalation_terms": ["민원", "분쟁", "환불 거절", "피해"],
    }
    write_python_pack(
        base,
        "stage03",
        """
        # Stage 03 Python

        룰 엔진만 분리한 pack이다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: regex DSL 없음
        """,
        """
        [project]
        name = "study2-stage03"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "data/rules.json": json.dumps(rules, ensure_ascii=False, indent=2),
            "src/stage03/guardrails.py": """
            import json
            from pathlib import Path


            def load_rules(path: Path) -> dict[str, list[str]]:
                return json.loads(path.read_text(encoding='utf-8'))


            def evaluate(user_message: str, assistant_response: str, rules: dict[str, list[str]]) -> list[str]:
                failures: list[str] = []
                if any(term in user_message for term in ['해지', '환불', '명의변경']) and '본인확인' not in assistant_response:
                    failures.append('MISSING_MANDATORY_STEP')
                if any(term in assistant_response for term in rules['forbidden_promises']):
                    failures.append('UNSUPPORTED_CLAIM')
                if any(term in assistant_response for term in rules['pii_patterns']):
                    failures.append('PII_EXPOSURE')
                if any(term in user_message for term in rules['escalation_terms']) and not any(term in assistant_response for term in ['상담원', '전문 부서']):
                    failures.append('ESCALATION_MISS')
                return failures
            """,
            "tests/test_guardrails.py": """
            from pathlib import Path

            from stage03.guardrails import evaluate, load_rules


            RULES = load_rules(Path('data/rules.json'))


            def test_mandatory_notice_rule():
                assert 'MISSING_MANDATORY_STEP' in evaluate('해지하려면?', '절차를 안내드리겠습니다.', RULES)


            def test_forbidden_promise_rule():
                assert 'UNSUPPORTED_CLAIM' in evaluate('할인돼요?', '무조건 가능합니다.', RULES)


            def test_pii_rule():
                assert 'PII_EXPOSURE' in evaluate('입력할까요?', '주민번호 990101-1234567 입력하세요.', RULES)


            def test_escalation_rule():
                assert 'ESCALATION_MISS' in evaluate('분쟁 접수하고 싶어요', '정책만 안내드립니다.', RULES)
            """,
        },
    )


def materialize_stage_04() -> None:
    base = stage_root("04-claim-and-evidence-pipeline")
    write_common_docs(
        base,
        "Stage 04 Claim And Evidence",
        "claim extraction, retrieval trace, verdict trace를 남기는 evidence pipeline pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["claim trace", "retrieval trace and verdict trace"],
        ["LLM provider 없음"],
    )
    write_python_pack(
        base,
        "stage04",
        """
        # Stage 04 Python

        claim/evidence trace를 독립 검증한다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: vector DB 없음
        """,
        """
        [project]
        name = "study2-stage04"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "src/stage04/pipeline.py": """
            def extract_claims(text: str) -> list[dict[str, str]]:
                sentences = [part.strip() for part in text.replace('?', '.').split('.') if part.strip()]
                return [{'claim_id': f'claim-{index}', 'statement': sentence} for index, sentence in enumerate(sentences, start=1)]


            def verify_claims(claims: list[dict[str, str]], kb: dict[str, str]) -> dict[str, object]:
                claim_results = []
                for claim in claims:
                    matched = [doc_id for doc_id, content in kb.items() if any(token in content for token in claim['statement'].split())]
                    verdict = 'support' if matched else 'not_found'
                    claim_results.append(
                        {
                            'claim_id': claim['claim_id'],
                            'verdict': verdict,
                            'evidence_doc_ids': matched[:2],
                            'retrieval_trace': {'query': claim['statement'], 'docs': matched[:3]},
                        }
                    )
                return {'claim_results': claim_results}
            """,
            "tests/test_pipeline.py": """
            from stage04.pipeline import extract_claims, verify_claims


            def test_claim_pipeline_keeps_retrieval_trace():
                claims = extract_claims('환불은 본인확인 후 접수 가능합니다. 상담원 연결이 필요할 수 있습니다.')
                kb = {'refund_policy.md': '환불은 본인확인 후 접수 가능합니다.'}
                result = verify_claims(claims, kb)
                assert result['claim_results'][0]['verdict'] == 'support'
                assert result['claim_results'][0]['retrieval_trace']['docs'] == ['refund_policy.md']
            """,
        },
    )


def materialize_stage_05() -> None:
    base = stage_root("05-judge-and-score-merge")
    write_common_docs(
        base,
        "Stage 05 Judge And Score",
        "judge output와 weighted score merge를 분리한 pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["heuristic judge", "score merge contract"],
        ["LLM adapter 없음"],
    )
    write_python_pack(
        base,
        "stage05",
        """
        # Stage 05 Python

        judge와 scorer의 합성만 검증한다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: live provider 없음
        """,
        """
        [project]
        name = "study2-stage05"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "src/stage05/judge.py": """
            def judge_response(user_message: str, assistant_response: str, failures: list[str]) -> dict[str, object]:
                correctness = 90.0 - len(failures) * 10
                resolution = 85.0 if len(assistant_response) > 10 else 70.0
                communication = 85.0 if '안내' in assistant_response or '확인' in assistant_response else 75.0
                return {
                    'correctness': max(correctness, 0.0),
                    'resolution': resolution,
                    'communication': communication,
                    'failure_types': sorted(set(failures)),
                }


            def merge_score(judgment: dict[str, object], groundedness: float, compliance: float) -> float:
                return round(
                    float(judgment['correctness']) * 0.30
                    + groundedness * 0.25
                    + compliance * 0.20
                    + float(judgment['resolution']) * 0.15
                    + float(judgment['communication']) * 0.10,
                    2,
                )
            """,
            "tests/test_judge.py": """
            from stage05.judge import judge_response, merge_score


            def test_judge_and_score_merge():
                judgment = judge_response('환불 안내', '환불 정책을 확인해 안내드리겠습니다.', [])
                total = merge_score(judgment, groundedness=90.0, compliance=100.0)
                assert total > 85
                assert judgment['failure_types'] == []
            """,
        },
    )


def materialize_stage_06() -> None:
    base = stage_root("06-golden-set-and-regression")
    write_common_docs(
        base,
        "Stage 06 Golden Regression",
        "golden case, replay runner, version compare input manifest를 분리한 regression pack이다.",
        ["cd python && UV_PYTHON=python3.12 uv run pytest -q"],
        ["golden assertion", "replay summary and compare manifest"],
        ["DB-backed dashboard 없음"],
    )
    write_python_pack(
        base,
        "stage06",
        """
        # Stage 06 Python

        golden case와 compare manifest를 소형 데이터로 유지한다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: full capstone report UI 없음
        """,
        """
        [project]
        name = "study2-stage06"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = []

        [dependency-groups]
        dev = ["pytest>=9.0.0"]
        """,
        {
            "data/golden_cases.json": json.dumps(
                {
                    "cases": [
                        {"id": "gs-001", "required_evidence_doc_ids": ["refund_policy.md"]},
                        {"id": "gs-002", "required_evidence_doc_ids": ["identity_verification.md"]},
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            "data/compare_manifest.json": json.dumps(
                {"baseline": "v1.0", "candidate": "v1.1", "dataset": "golden-set"},
                ensure_ascii=False,
                indent=2,
            ),
            "src/stage06/regression.py": """
            import json
            from pathlib import Path


            def evaluate_case(required_doc_ids: list[str], actual_doc_ids: list[str]) -> dict[str, object]:
                passed = any(doc_id in actual_doc_ids for doc_id in required_doc_ids)
                return {'passed': passed, 'reason_codes': [] if passed else ['MISSING_REQUIRED_EVIDENCE_DOC']}


            def load_manifest(path: Path) -> dict[str, str]:
                return json.loads(path.read_text(encoding='utf-8'))
            """,
            "tests/test_regression.py": """
            from pathlib import Path

            from stage06.regression import evaluate_case, load_manifest


            def test_golden_assertion_and_compare_manifest():
                assert evaluate_case(['refund_policy.md'], ['refund_policy.md'])['passed'] is True
                manifest = load_manifest(Path('data/compare_manifest.json'))
                assert manifest['baseline'] == 'v1.0'
                assert manifest['candidate'] == 'v1.1'
            """,
        },
    )


def materialize_stage_07() -> None:
    base = stage_root("07-monitoring-dashboard-and-review-console")
    write_common_docs(
        base,
        "Stage 07 Monitoring Console",
        "overview/failures/session review/eval runner/version compare를 보여주는 focused API + React pack이다.",
        [
            "cd python && UV_PYTHON=python3.12 uv run pytest -q",
            "cd react && pnpm test --run",
        ],
        ["FastAPI snapshot endpoints", "React dashboard pages and mocked tests"],
        ["실제 DB persistence 없음"],
    )
    write_python_pack(
        base,
        "stage07",
        """
        # Stage 07 Python

        FastAPI snapshot server로 dashboard contracts를 독립 검증한다.

        - build: `UV_PYTHON=python3.12 uv sync`
        - test: `UV_PYTHON=python3.12 uv run pytest -q`
        - current status: verified
        - known gaps: persistent storage 없음
        """,
        """
        [project]
        name = "study2-stage07"
        version = "0.1.0"
        requires-python = ">=3.12,<3.13"
        dependencies = ["fastapi>=0.115.0", "pydantic>=2.9.0"]

        [dependency-groups]
        dev = ["httpx>=0.27.2", "pytest>=9.0.0"]
        """,
        {
            "src/stage07/app.py": """
            from fastapi import FastAPI

            app = FastAPI()

            SNAPSHOT = {
                'overview': {'avg_score': 87.76, 'fail_rate': 0.0, 'critical_count': 0, 'evaluation_count': 30, 'avg_latency_ms': 112.4, 'grade_distribution': {'A': 19, 'B': 11}, 'failure_top': [], 'run_labels': ['v1.0', 'v1.1']},
                'failures': {'items': [{'failure_type': 'MISSING_REQUIRED_EVIDENCE_DOC', 'count': 11, 'critical_count': 0, 'avg_score': 66.0}]},
                'conversations': {'items': [{'id': 'conv-001', 'created_at': '2026-03-07T00:00:00+00:00', 'prompt_version': 'v1.0', 'kb_version': 'v1.1', 'run_id': 'run-001', 'turn_count': 1, 'session_score': 90.0, 'session_grade': 'A'}]},
                'conversation_detail': {'conversation': {'id': 'conv-001', 'created_at': '2026-03-07T00:00:00+00:00', 'prompt_version': 'v1.0', 'kb_version': 'v1.1', 'run_id': 'run-001', 'turn_count': 1, 'session_score': 90.0, 'session_grade': 'A'}, 'turns': [{'id': 'turn-001', 'turn_index': 1, 'user_message': '환불 접수 전에 인증 필수인가요?', 'assistant_response': '환불은 본인확인 후 접수 가능하며, 인증 실패 시 상담원 연결 후 추가 확인 절차를 진행합니다.', 'retrieved_doc_ids': ['refund_policy.md', 'identity_verification.md'], 'evaluation': {'id': 'eval-001', 'grade': 'A', 'total_score': 90.0, 'failure_types': [], 'lineage': {'run_label': 'v1.1', 'dataset': 'golden-set', 'trace_id': 'trace-001', 'retrieval_version': 'retrieval-v2'}, 'judge_trace': {'provider': 'heuristic', 'model': 'judge-v2', 'short_circuit': False, 'short_circuit_reason': None}}}]},
                'golden_run': {'run_id': 'run-001', 'run_label': 'v1.1', 'dataset': 'golden-set', 'count': 30, 'avg_score': 87.76, 'critical_count': 0, 'pass_count': 19, 'fail_count': 11},
                'compare': {'result': {'baseline': 'v1.0', 'candidate': 'v1.1', 'dataset': 'golden-set', 'baseline_avg': 84.06, 'candidate_avg': 87.76, 'baseline_critical': 2, 'candidate_critical': 0, 'baseline_pass_count': 16, 'candidate_pass_count': 19, 'baseline_fail_count': 14, 'candidate_fail_count': 11, 'baseline_failures': {'MISSING_REQUIRED_EVIDENCE_DOC': 14}, 'candidate_failures': {'MISSING_REQUIRED_EVIDENCE_DOC': 11}, 'delta': 3.7, 'pass_delta': 3, 'fail_delta': -3, 'critical_delta': -2}},
            }


            @app.get('/api/dashboard/overview')
            def overview() -> dict[str, object]:
                return SNAPSHOT['overview']


            @app.get('/api/dashboard/failures')
            def failures() -> dict[str, object]:
                return SNAPSHOT['failures']


            @app.get('/api/conversations')
            def conversations() -> dict[str, object]:
                return SNAPSHOT['conversations']


            @app.get('/api/conversations/{conversation_id}')
            def conversation_detail(conversation_id: str) -> dict[str, object]:
                assert conversation_id == 'conv-001'
                return SNAPSHOT['conversation_detail']


            @app.post('/api/golden-set/run')
            def golden_run() -> dict[str, object]:
                return SNAPSHOT['golden_run']


            @app.get('/api/dashboard/version-compare')
            def version_compare() -> dict[str, object]:
                return SNAPSHOT['compare']
            """,
            "tests/test_api.py": """
            from fastapi.testclient import TestClient

            from stage07.app import app


            client = TestClient(app)


            def test_dashboard_snapshot_endpoints():
                assert client.get('/api/dashboard/overview').status_code == 200
                assert client.get('/api/dashboard/failures').json()['items'][0]['failure_type'] == 'MISSING_REQUIRED_EVIDENCE_DOC'
                assert client.get('/api/conversations/conv-001').json()['turns'][0]['evaluation']['lineage']['run_label'] == 'v1.1'
                assert client.post('/api/golden-set/run').json()['avg_score'] == 87.76
                assert client.get('/api/dashboard/version-compare').json()['result']['delta'] == 3.7
            """,
        },
    )
    copytree(V1_REACT, base / "react")
    write(
        base / "react" / "README.md",
        """
        # Stage 07 React

        `08/v1-regression-hardening/react`의 dashboard slice를 그대로 복제한 focused UI pack이다.

        - build: `pnpm install`
        - test: `pnpm test --run`
        - current status: verified through copied mocked tests
        - known gaps: stage07/python snapshot API를 직접 바라보도록 env wiring은 사용자가 지정해야 한다.
        """,
    )


def write_capstone_public_docs() -> None:
    base = ROOT / "08-capstone-submission"
    meta = STAGE_META["08-capstone-submission"]
    problem = (
        "# Capstone Problem\n\n"
        f"{meta['summary']}\n\n"
        "## Stage Question\n\n"
        f"{meta['stage_question']}\n\n"
        "## Inputs\n\n"
        f"{bullet_list(meta['inputs'])}\n\n"
        "## Required Output\n\n"
        f"{bullet_list(meta['outputs'])}\n\n"
        "## Success Criteria\n\n"
        f"{bullet_list(meta['success'])}\n"
    )
    docs = (
        "# Capstone Docs\n\n"
        "이 디렉터리는 capstone 버전 공통 문서와 시연 자료를 보관한다.\n\n"
        "## Version Roles\n\n"
        "- `v0-*`: runnable baseline과 local heuristic path 정리\n"
        "- `v1-*`: provider fallback, lineage/trace, PostgreSQL smoke, version compare hardening\n"
        "- `v2-*`: retrieval improvement proof와 제출용 artifact 마감\n\n"
        "## Concept Focus\n\n"
        f"{bullet_list(meta['concepts'])}\n\n"
        "## Verification Snapshot\n\n"
        f"{bullet_list(meta['verification_notes'])}\n\n"
        "## Read In This Order\n\n"
        "- `README.md`\n"
        "- `docs/release-readiness.md`\n"
        "- `v0-*/README.md`, `v1-*/README.md`, `v2-*/README.md`\n"
        "- `v2-submission-polish/docs/demo/proof-artifacts/`\n\n"
        "## Known Gap\n\n"
        "- live Upstage/OpenAI/Langfuse credential path는 기본 검증에 포함되지 않았다.\n"
        "- tracked 문서는 stable index 역할을 하고, 세부 process log는 local-only `notion/`에 남긴다.\n"
    )
    write(base / "problem" / "README.md", problem)
    write(base / "docs" / "README.md", docs)


def materialize_notion() -> None:
    targets = [
        "00-source-brief",
        "01-quality-rubric-and-score-contract",
        "02-domain-fixtures-and-chat-harness",
        "03-rule-and-guardrail-engine",
        "04-claim-and-evidence-pipeline",
        "05-judge-and-score-merge",
        "06-golden-set-and-regression",
        "07-monitoring-dashboard-and-review-console",
        "08-capstone-submission",
    ]
    for target in targets:
        meta = STAGE_META[target]
        notion = ROOT / target / "notion"
        notion.mkdir(parents=True, exist_ok=True)
        title = target
        write(
            notion / "00-problem-framing.md",
            (
                f"# {title} Problem Framing\n\n"
                "## Goal\n\n"
                f"{meta['summary']}\n\n"
                "## Success Criteria\n\n"
                f"{bullet_list(meta['success'])}\n\n"
                "## Prerequisites\n\n"
                f"{bullet_list(meta['prerequisites'])}\n\n"
                "## Evidence To Check\n\n"
                f"{bullet_list(meta['evidence'])}\n\n"
                "## Uncertainty\n\n"
                f"{meta['uncertainty']}\n"
            ),
        )
        write(
            notion / "01-approach-log.md",
            (
                f"# {title} Approach Log\n\n"
                "## Stage Question\n\n"
                f"{meta['stage_question']}\n\n"
                "## Chosen Direction\n\n"
                f"{render_decisions(meta['decisions'])}\n\n"
                "## Alternatives Rejected\n\n"
                f"{bullet_list(meta['rejected'])}\n\n"
                "## Why This Fits The Curriculum\n\n"
                f"{bullet_list(meta['capstone_mapping'])}\n"
            ),
        )
        write(
            notion / "02-debug-log.md",
            (
                f"# {title} Debug Log\n\n"
                "## Verification Notes\n\n"
                f"{bullet_list(meta['verification_notes'])}\n\n"
                "## Failure Cases And Fixes\n\n"
                f"{render_debug_cases(meta['debug_cases'])}\n"
            ),
        )
        write(
            notion / "03-retrospective.md",
            (
                f"# {title} Retrospective\n\n"
                "## Strengthened Areas\n\n"
                f"{bullet_list(meta['strengths'])}\n\n"
                "## Remaining Weak Spots\n\n"
                f"{bullet_list(meta['weaknesses'])}\n\n"
                "## Revisit Later\n\n"
                f"{bullet_list(meta['revisit'])}\n"
            ),
        )
        write(
            notion / "04-knowledge-index.md",
            (
                f"# {title} Knowledge Index\n\n"
                "## Core Concepts\n\n"
                f"{bullet_list(meta['concepts'])}\n\n"
                "## References\n\n"
                f"{render_knowledge(meta['knowledge'])}\n"
            ),
        )


def main() -> None:
    materialize_stage_00()
    materialize_stage_01()
    materialize_stage_02()
    materialize_stage_03()
    materialize_stage_04()
    materialize_stage_05()
    materialize_stage_06()
    materialize_stage_07()
    write_capstone_public_docs()
    materialize_notion()


if __name__ == "__main__":
    main()
