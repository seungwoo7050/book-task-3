> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# Capstone — 접근 기록

## v0 → v1: provider chain 도입

v0에서 heuristic judge만 사용했을 때, "실제 LLM을 쓰면 결과가 어떻게 달라지나?"라는 질문에 답할 수 없었다.

provider chain의 설계:
1. 1차: Upstage Solar — 한국어 성능이 좋음
2. 2차: OpenAI — Solar 실패 시 fallback
3. 3차: Ollama — 외부 API 전부 실패 시 로컬 fallback

chain의 핵심 규칙:
- 각 provider가 timeout이나 에러를 반환하면 다음 provider로 넘어간다
- 모든 provider가 실패하면 heuristic으로 최종 fallback한다
- 어떤 provider가 실행되었는지 `judge_trace`에 기록한다

이 결정의 장점: 외부 API key 없이도 시스템이 동작한다. Ollama가 없어도 heuristic이 있다.
단점: chain 순서를 런타임에 바꿀 수 없다 (하드코딩).

## v1 → v2: retrieval-v2 개선

v1까지 retrieval은 keyword matching이었다.
v2에서 세 가지를 추가했다:

1. **alias 매핑**: "환불" → "refund_policy.md", "본인확인" → "identity_verification.md"
2. **category 기반 필터링**: 문서에 카테고리 태그를 달아 관련 문서 우선 반환
3. **risk rerank**: 민감 주제(개인정보, 금융)에 해당하는 문서를 상위로 올림

이 개선의 효과를 같은 golden set으로 측정한 결과:
- avg_score: 84.06 → 87.76 (+3.7)
- critical_count: 2 → 0
- pass_count: 16 → 19 (+3)
- fail_count: 14 → 11 (-3)

이 수치가 capstone의 핵심 증거다. "코드를 바꿨더니 실제로 좋아졌다"를 golden set이 보여준다.

## v2 → v3: self-hosted 패키징

v2까지는 개발자 로컬에서 실행하는 것을 전제했다.
v3부터는 "다른 팀이 받아서 바로 쓸 수 있어야 한다"가 목표다.

새로 추가된 것:
- **관리자 인증**: email/password 기반 단일 관리자 로그인
- **데이터 업로드 UI**: transcript JSONL, KB bundle ZIP
- **비동기 job**: evaluation 요청을 큐에 넣고 worker가 처리
- **Docker Compose**: 한 명령으로 전체 배포
- **optional AI profile**: `--profile ai`로 ollama/chroma 컨테이너 추가

Docker Compose 구성:
```yaml
services:
  api:       # FastAPI 서버
  web:       # React 프론트엔드
  db:        # PostgreSQL
  worker:    # evaluation worker
  # optional:
  ollama:    # local LLM
  chroma:    # vector store
```
