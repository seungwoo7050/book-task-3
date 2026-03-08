# Capstone Presentation Materials

이 디렉터리는 `v0`, `v1`, `v2` 각각을 독립 발표로 설명할 수 있도록 만든 발표용 Markdown 문서를 모은다.

핵심 질문은 하나다.

- `이걸로 그래서 뭘 할 수 있는데?`

각 문서는 이 질문에 서로 다른 수준으로 답한다.

- `v0`: 배포 직전 품질 게이트를 실제로 돌릴 수 있다.
- `v1`: 운영자가 장애와 품질 원인을 추적하고 대응할 수 있다.
- `v2`: 개선 후보를 baseline과 비교해 배포 여부를 숫자로 결정할 수 있다.

## Documents

- [`v0 발표 문서`](../../v0-initial-demo/docs/presentation/v0-demo-presentation.md)
- [`v1 발표 문서`](../../v1-regression-hardening/docs/presentation/v1-demo-presentation.md)
- [`v2 발표 문서`](../../v2-submission-polish/docs/presentation/v2-demo-presentation.md)

## Evidence Policy

- 화면 캡처는 각 버전의 `docs/demo/scenario-artifacts/*.png`를 사용한다.
- CLI/API 증빙은 각 버전의 `docs/demo/proof-artifacts/*`를 사용한다.
- 문서 안에는 캡처 시점과 proof 재생성 시점을 분리해 적는다.

## Recommended Order

1. `v0`: end-to-end baseline이 실제로 돌아간다는 점을 보여준다.
2. `v1`: 같은 사용 흐름 위에 운영 안정성과 traceability를 추가한 이유를 설명한다.
3. `v2`: retrieval 개선이 실제 품질 향상으로 이어졌음을 수치로 닫는다.
