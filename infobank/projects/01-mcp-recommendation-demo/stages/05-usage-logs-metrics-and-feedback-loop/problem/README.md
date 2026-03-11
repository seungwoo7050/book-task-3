# 05 로그, 지표, 피드백 루프 문제 정의

## 문제 해석

usage event, feedback record, experiment metadata를 DB와 API로 연결해 추천 품질 개선의 운영 루프를 설명하는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- usage tables
- feedback loop
- experiment console API

## 완료 기준

- 추천 품질 개선이 일회성 실험이 아니라 운영 루프로 설명된다.
- 학생이 자기 프로젝트에서 어떤 운영 지표를 남겨야 할지 감을 잡는다.
- 후속 release gate와 operator console 단계로 자연스럽게 이어진다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/db/schema.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

## 범위 메모

- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.
