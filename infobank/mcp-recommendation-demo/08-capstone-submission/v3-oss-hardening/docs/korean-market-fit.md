# Korean Market Fit

`study1` 전체 주제가 한국어 MCP 추천 최적화이므로, `v3`에서도 self-hosted 운영자가 한국어로 추천 근거와 release proof를 읽을 수 있어야 한다.

## Why It Matters

- 운영자 설명이 영어-only면 추천 수용 근거가 약해진다.
- release gate 결과를 팀 내부 문서로 옮길 때 한국어 문장이 필요하다.
- self-hosted 환경에서는 외부 LLM 없이 deterministic explanation이 더 재현 가능하다.

## v3 Fit

- recommendation explanation은 한국어 템플릿으로 유지된다.
- audit/detail text도 한국어 중심으로 저장된다.
- release artifact는 Markdown으로 export되어 팀 문서로 옮기기 쉽다.
