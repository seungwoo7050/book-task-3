# capstone 제출 정리 회고

## 이번 stage로 좋아진 점

- 학생이 baseline, hardening, submission polish, OSS hardening을 단계별로 읽을 수 있다.
- 제출용 버전과 제품화 확장 버전을 분리해 포트폴리오 설명이 쉬워졌다.
- `05-development-timeline.md`를 중심으로 어떤 순서로 재현해야 하는지 한 번에 따라갈 수 있다.

## 아직 약한 부분

- live provider나 실제 운영 환경 smoke run은 기본 경로에 포함되지 않는다.
- 일부 깊은 시행착오는 여전히 `notion-archive/`에 더 많이 남아 있다.
- 버전별 proof 문서 중 몇 개는 명령과 acceptance 기준은 명확하지만, 왜 그 기준을 골랐는지까지는 아직 더 설명할 수 있다.

## 학생이 여기서 바로 가져갈 것

- `v0 -> v3` 스냅샷 전략으로 제출 버전과 제품화 확장 버전을 한 레포 안에서 분리하는 방식
- compare, compatibility, release gate, artifact export를 발표와 제출 증빙까지 이어지는 공개 문서 구조로 묶는 방식

## 05-development-timeline.md와 같이 읽을 포인트

- 먼저 `v2`를 최종 제출 기준선으로 재현한 뒤, `v0`, `v1`, `v3`를 비교하는 순서를 유지한다.
- 자기 포트폴리오 레포에 옮길 때도 이 타임라인의 체크포인트를 acceptance checklist로 다시 쓰면 좋다.

## 나중에 다시 볼 것

- `v3` 이후 실제 배포/운영 지표가 생기면 별도 운영 부록을 만들 수 있다.
- 발표 자료와 캡처 재생성을 더 자동화할 수 있다.
- 학생 포트폴리오용 파생 레포를 만든다면 `v2`를 최소 제출선, `v3`를 선택형 확장 부록으로 분리하는 편이 읽기 좋다.
