# Study Workspace

`study/`는 이 저장소의 실제 학습 트리다. 새 구조는 기술 카테고리보다 학습 단계가 먼저 보이도록
`foundations -> architecture -> product-systems -> capstone` 순서로 정리한다.

## 읽는 방법

1. stage README에서 왜 이 단계가 필요한지 본다.
2. 프로젝트 README에서 `문제 / 내 답 / 검증 / 읽는 순서`를 본다.
3. 세부 요구사항은 `problem/README.md`, 구현 세부는 `react-native/README.md`와 `node-server/README.md`를 본다.
4. 긴 시행착오는 `notion/README.md` 아래 문서를 본다.

## Stages

### [foundations](foundations/README.md)

- [01-navigation-patterns](foundations/01-navigation-patterns/README.md)
- [02-virtualized-list-performance](foundations/02-virtualized-list-performance/README.md)
- [03-gestures-and-reanimated](foundations/03-gestures-and-reanimated/README.md)

핵심 질문:
- 화면 구조와 deep link state를 어떻게 통제하는가
- 대량 리스트를 어떻게 측정하고 비교하는가
- 제스처와 애니메이션을 UI thread 중심으로 어떻게 설계하는가

### [architecture](architecture/README.md)

- [01-bridge-vs-jsi](architecture/01-bridge-vs-jsi/README.md)
- [02-native-modules](architecture/02-native-modules/README.md)

핵심 질문:
- RN runtime 경계의 비용 차이를 어떻게 계측하는가
- JS/native 계약을 어떤 문서와 spec으로 고정하는가

### [product-systems](product-systems/README.md)

- [01-offline-sync-foundations](product-systems/01-offline-sync-foundations/README.md)
- [02-realtime-chat](product-systems/02-realtime-chat/README.md)
- [03-app-distribution](product-systems/03-app-distribution/README.md)

핵심 질문:
- local-first 제품 모델을 어떤 순서로 쌓아 올리는가
- release rehearsal을 별도 과제로 분리하면 무엇이 선명해지는가

### [capstone](capstone/README.md)

- [01-incident-ops-mobile](capstone/01-incident-ops-mobile/README.md)
- [02-incident-ops-mobile-client](capstone/02-incident-ops-mobile-client/README.md)

핵심 질문:
- system/contract 증명과 hiring-facing 제품 완성작을 어떻게 분리하는가
- 동일 도메인을 두 번 구현할 때 어떤 학습 가치가 생기는가

## 공통 규약

- 프로젝트 README는 `문제 / 내 답 / 검증 / 읽는 순서 / 상태`를 반드시 가진다.
- `problem/README.md`는 한국어 문제 정의의 단일 진입점이다.
- `docs/`는 안정적인 개념 문서, `notion/`은 상세 학습 로그다.
- 구현 디렉터리 이름은 `react-native/`, capstone 백엔드는 `node-server/`를 유지한다.

## 검증

```bash
bash ../scripts/check_study_docs.sh
bash ../scripts/verify_study_structure.sh
bash ../scripts/report_study_status.sh
```
