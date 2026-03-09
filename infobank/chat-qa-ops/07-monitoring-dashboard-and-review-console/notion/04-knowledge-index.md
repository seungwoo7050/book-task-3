# Monitoring Dashboard — 지식 인덱스

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/dashboard/overview` | GET | 평균 점수, 실패율, critical 건수, 등급 분포, run_labels |
| `/api/dashboard/failures` | GET | failure_type별 발생 건수, critical 비율, 평균 점수 |
| `/api/conversations` | GET | 상담 세션 목록 (id, score, grade 등) |
| `/api/conversations/{id}` | GET | 세션 상세: 턴 목록 + 각 턴의 evaluation (lineage, judge_trace) |
| `/api/golden-set/run` | POST | golden set 실행 결과 반환 |
| `/api/dashboard/version-compare` | GET | baseline vs candidate 비교 결과 (delta, pass/fail 변화) |

## 핵심 개념

| 개념 | 설명 | 관련 코드 |
|------|------|-----------|
| SNAPSHOT | 모든 API 응답 데이터를 담은 정적 dict. DB 없이 API 계약을 확정하기 위한 것 | `app.py → SNAPSHOT` |
| lineage | 평가의 실행 환경 메타데이터: run_label, dataset, trace_id, retrieval_version | `SNAPSHOT['conversation_detail']` |
| judge_trace | 어떤 judge로 채점했는지: provider(heuristic/llm), model, short_circuit 여부 | `SNAPSHOT['conversation_detail']` |
| version compare | baseline과 candidate의 golden set 실행 결과를 비교. delta, pass_delta, critical_delta 등 | `SNAPSHOT['compare']` |
| grade_distribution | 등급별 건수 분포. 현재: A=19, B=11 | `SNAPSHOT['overview']` |

## React 페이지 구조

| 페이지 | 파일 | 기능 |
|--------|------|------|
| 개요 | `pages/Overview.tsx` | ScoreCard + version compare + grade 분포 |
| 실패 분석 | `pages/Failures.tsx` | FailureTable 컴포넌트로 failure_type별 정보 표시 |
| 세션 리뷰 | `pages/SessionReview.tsx` | 세션 목록 → 클릭 → 턴별 상세(evaluation + lineage) |
| 평가 실행 | `pages/EvalRunner.tsx` | golden run 트리거 버튼 + 결과 표시 |

## 기술 스택

- **Backend**: FastAPI, Python 3.12, uvicorn
- **Frontend**: React 18, TypeScript, Vite, React Router, Vitest + Testing Library
- **상태 관리**: useState + useEffect (별도 라이브러리 없음)
- **스타일**: CSS (styles.css)
- **i18n**: 수동 매핑 (i18n/ko.ts)

## 다음 단계 연결

- **capstone v0**: SNAPSHOT을 SQLite 기반 실제 데이터로 교체
- **capstone v1**: PostgreSQL + provider chain으로 전환, lineage 자동 기록
- **capstone v3**: auth/RBAC 추가, Docker Compose로 전체 배포
