# Bomb Lab phase 패턴 지도

## 이 문서가 필요한 이유

Bomb Lab을 처음 보면 여섯 phase가 모두 다른 문제처럼 보입니다.
하지만 실제로는 기계어 수준에서 반복해서 등장하는 구조들을 묻고 있습니다.

## 주요 패턴과 읽는 포인트

| 패턴 | 무엇을 읽어야 하는가 | companion 구현에서 대응하는 것 |
|---|---|---|
| 직접 문자열 비교 | 고정 문자열 주소와 비교 루프 | exact phrase validation |
| 루프 기반 수열 | 반복 관계와 누적 상태 | doubling sequence |
| jump table | 인덱스 기반 분기와 case별 상수 | switch 기반 value mapping |
| 재귀 경로 인코딩 | midpoint 계산과 반환값 조합 | `func4` 스타일 path check |
| nibble lookup | `input[i] & 0xf`와 정적 테이블 | 6글자 masked lookup |
| 연결 리스트 재배열 | pointer chase와 재연결 후 정렬 조건 | `7 - x` 변환 후 descending check |
| secret BST walk | 트리 탐색과 경로 인코딩 | `fun7` 스타일 tree traversal |

## 왜 패턴 이름을 붙이는가

패턴 이름이 생기면 phase를 "정답 문자열"이 아니라 "구조"로 기억하게 됩니다.
이것이 공개 저장소에서 답을 줄이면서도 학습 가치를 유지하는 핵심입니다.

## companion 구현용 정답 예시를 어떻게 봐야 하나

이 저장소의 companion mini-bomb은 다음 입력으로 검증합니다.

- Phase 1: `Assembly reveals intent.`
- Phase 2: `1 2 4 8 16 32`
- Phase 3: 예시 `1 311`
- Phase 4: `6 6`
- Phase 5: `01234.`
- Phase 6: `4 6 2 3 5 1`
- Secret: `35`

이 값들은 companion 구현용 검증 데이터일 뿐이며, 어떤 공식 course bomb의 정답이라고 주장하지 않습니다.

## 공개 저장소에서 어디까지 설명할 것인가

설명해도 되는 것:

- 패턴 이름
- 분석 순서
- 각 패턴이 강제하는 불변식
- companion 구현이 어떤 패턴을 복제했는지

설명하지 않는 편이 좋은 것:

- 특정 비공개 bomb의 raw answer
- line-by-line disassembly dump
- 외부 course 자산 재배포
