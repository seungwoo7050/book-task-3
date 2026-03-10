# capstone 문서 안내

이 폴더는 versioned capstone 전체를 설명하는 안정적인 인덱스다. 추천 로직, 실험, 제출 증빙, self-hosted 확장을 어떤 순서로 읽어야 하는지 정리한다.

## 포함 내용

- `v0-initial-demo/docs/README.md`
- `v1-ranking-hardening/docs/README.md`
- `v2-submission-polish/docs/README.md`
- `v3-oss-hardening/docs/README.md`
- 각 버전의 발표 문서와 시연 자료

## 읽는 순서

1. `v0`에서 baseline selector와 offline eval을 본다.
2. `v1`에서 rerank, feedback, compare 운영 루프를 본다.
3. `v2`에서 release gate와 submission proof로 capstone을 닫는다.
4. `v3`에서 self-hosted OSS로 가기 위해 auth, jobs, audit, Compose가 어떻게 추가됐는지 확인한다.

## 학생 관점에서 보면 좋은 점

- 작은 추천 데모를 운영형 시스템으로 넓혀 가는 설명 방식을 참고할 수 있다.
- 각 버전이 무엇을 증명하는지 README만으로 구분하는 방식을 따라갈 수 있다.
- 발표 자료와 제품 문서를 같은 레포 안에 정리하는 법을 볼 수 있다.

## 학생이 이 문서 묶음에서 바로 가져갈 것

- `README.md`, `problem/README.md`, `docs/README.md`, `notion/05-development-timeline.md`를 서로 다른 공개 역할로 나누는 방식
- 현재 단계의 검증 명령과 acceptance 기준을 짧은 공개 문서로 남기는 방식
- 장문 시행착오는 `notion/`으로 보내고, 오래 남길 개념과 증빙만 tracked docs에 남기는 방식

## notion과 05 타임라인을 읽는 법

- 빠른 현재 상태는 tracked docs에서 먼저 확인한다.
- 같은 결과를 다시 재현하려면 `../notion/05-development-timeline.md`를 따라 읽고 실행한다.
- 새 기준으로 다시 쓰고 싶다면 기존 `notion/`을 `../notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
