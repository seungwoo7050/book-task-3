# 07 운영자 대시보드와 실험 콘솔 문제 정의

## 문제 해석

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 정리해 추천 시스템의 운영 면을 보여 주는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- operator dashboard
- experiment console
- release console

## 완료 기준

- 추천 시스템이 단일 API가 아니라 운영 도구까지 포함한다는 점을 보여 준다.
- 학생이 자기 포트폴리오에서 운영자 UI를 어떻게 설명할지 참고할 수 있다.
- 최종 capstone의 화면 중심 시연 경로가 명확해진다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`

## 범위 메모

- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.
