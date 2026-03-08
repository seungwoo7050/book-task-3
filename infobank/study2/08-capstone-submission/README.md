# Study 2 Capstone

이 capstone은 상담 품질 평가 파이프라인과 운영 대시보드를 묶어 제출 가능한 데모로 마감하는 프로젝트다.

## Core Promise

- 상담 품질을 한국어 기준으로 정의한다.
- rule/guardrail, evidence verifier, judge scoring을 합성한다.
- golden replay와 dashboard로 품질을 설명한다.
- 개선 실험이 실제로 효과가 있었는지 비교 증빙을 남긴다.

## Version Rule

1. `v0-initial-demo`: 최초 제출 가능한 QA Ops 데모
2. `v1-regression-hardening`: `v0` 복제 후 lineage/version compare와 안정성 강화
3. `v2-submission-polish`: `v1` 복제 후 개선 실험 증빙과 제출 시연 마감
4. `v3-self-hosted-oss`: `v2` 복제 후 single-team self-hosted OSS snapshot으로 승격

모든 버전은 폴더 단위 스냅샷이다.
기존 버전을 수정하지 않고 다음 버전 폴더를 복제해 작업한다.

현재 self-hosted 사용 권장 버전은 [`v3-self-hosted-oss`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v3-self-hosted-oss/README.md)다. `v0~v2`는 archive/demo 및 발표 증빙 역할을 유지한다.

## Release Note

공개 저장소 기준 검증 명령과 최종 compare 결과는 [`docs/release-readiness.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/docs/release-readiness.md)에 정리했다.

## Presentation Materials

- 발표 자료 인덱스: [`docs/presentations/README.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/docs/presentations/README.md)
- `v0` 발표 문서: [`v0-initial-demo/docs/presentation/v0-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v0-initial-demo/docs/presentation/v0-demo-presentation.md)
- `v1` 발표 문서: [`v1-regression-hardening/docs/presentation/v1-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v1-regression-hardening/docs/presentation/v1-demo-presentation.md)
- `v2` 발표 문서: [`v2-submission-polish/docs/presentation/v2-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/presentation/v2-demo-presentation.md)
