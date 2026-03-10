# Python 내부 문서 안내

`v3-self-hosted-oss`의 Python 문서는 self-hosted 환경에서도 backend job, evaluator, artifact 흐름을 유지하는 데 필요한 내부 설계 메모를 담는다. 설치 문서만으로 부족한 운영 관점의 세부 규칙을 보완하는 용도다.

## 이 버전에서 중요하게 볼 내용

- worker/job이 artifact export와 regression run을 어떤 순서로 수행하는지
- self-hosted storage와 local file artifact가 어떤 경계로 분리되는지
- dependency health와 운영자 review queue를 OSS 배포 기준에서 어떻게 해석하는지
- 공개 저장소로 옮겨도 남겨야 할 최소 telemetry와 audit trail이 무엇인지
