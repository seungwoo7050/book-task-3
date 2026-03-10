# 한국어 시장 적합성

`study1` 전체 주제가 한국어 MCP 추천 최적화이므로, `v3`에서도 self-hosted 운영자가 한국어로 추천 근거와 release proof를 읽을 수 있어야 한다.

## 왜 중요한가

- 운영자 설명이 영어-only면 추천 수용 근거가 약해진다.
- release gate 결과를 팀 내부 문서로 옮길 때 한국어 문장이 필요하다.
- self-hosted 환경에서는 외부 LLM 없이 deterministic explanation이 더 재현 가능하다.

## v3에서 어떻게 반영했는가

- recommendation explanation은 한국어 템플릿으로 유지된다.
- audit/detail text도 한국어 중심으로 저장된다.
- release artifact는 Markdown으로 export되어 팀 문서로 옮기기 쉽다.

## 검증 경로

- `pnpm eval`: 한국어 seeded query가 OSS 모드에서도 baseline recall을 유지하는지 확인한다.
- `pnpm compatibility rc-release-check-bot-1-5-0`: 한국어 metadata completeness가 self-hosted release candidate에도 동일하게 적용되는지 확인한다.
- `pnpm release:gate rc-release-check-bot-1-5-0`: OSS 배포 전에도 한국어 release proof와 risk 요약이 빠지지 않는지 확인한다.
