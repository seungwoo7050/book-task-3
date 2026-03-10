# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- System V AMD64 호출 규약: 인자 전달과 반환값 흐름을 읽어야 phase별 함수 의미를 복원할 수 있다.
- `explode_bomb` 기준 브레이크포인트 워크플로: 실패 지점을 먼저 고정해야 추측 대신 관찰로 넘어갈 수 있다.
- jump table 인식: `switch`류 phase를 if-chain으로 오해하지 않기 위한 첫 체크포인트다.
- 재귀 경로 인코딩: phase 4처럼 반환값이 경로를 담는 함수를 읽을 때 필요한 모델이다.
- 연결 리스트 재배열: phase 6에서는 포인터 재연결보다 입력 전처리와 순서 매핑을 먼저 봐야 한다.
- 공개 범위 판단: 분석이 잘 될수록 더 많이 공개하고 싶어지므로, raw answer와 구조 설명을 의식적으로 분리해야 한다.

## 재현 중 막히면 먼저 확인할 것

- 분석 워크플로: `../docs/concepts/reverse-engineering-workflow.md`
- phase별 패턴: `../docs/concepts/phase-patterns.md`
- 공개 경계: `../docs/references/publication-policy.md`
- 현재 검증 순서: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- `attacklab`에서도 답보다 구조를 먼저 본다는 원칙이 그대로 이어진다.
- 보안 계열 프로젝트는 구현만큼 문서 공개 범위 설계가 중요하다.
