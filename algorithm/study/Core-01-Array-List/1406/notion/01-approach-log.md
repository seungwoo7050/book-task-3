# 접근 로그

> 프로젝트: 에디터
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 발상: Two-Stack 모델

커서를 기준으로 왼쪽 문자열과 오른쪽 문자열을 각각 스택으로 관리한다.

- `left` 스택: 커서 왼쪽의 문자들 (top = 커서 바로 왼쪽)
- `right` 스택: 커서 오른쪽의 문자들 (top = 커서 바로 오른쪽)

이렇게 하면 모든 연산이 O(1)이다:
- **L (왼쪽 이동)**: left에서 pop → right에 push
- **D (오른쪽 이동)**: right에서 pop → left에 push
- **B (삭제)**: left에서 pop (버린다)
- **P x (삽입)**: left에 push

처음 이 아이디어를 봤을 때 "두 스택이 어떻게 커서를 표현하지?" 싶었다.
하지만 직접 예제를 그려 보면 명확해진다.

`abcd |` (커서가 끝에 있을 때)
- left = [a, b, c, d], right = []

`L` 실행 → `abc | d`
- left = [a, b, c], right = [d]

`P x` 실행 → `abcx | d`
- left = [a, b, c, x], right = [d]

## 왜 연결 리스트가 아닌가?

연결 리스트도 O(1) 삽입/삭제가 가능하다.
하지만 Python에서 연결 리스트를 직접 구현하면 node 생성의 오버헤드가 크다.
두 개의 Python list를 스택으로 쓰면 append/pop이 amortized O(1)이고, 구현도 훨씬 간단하다.

## 최종 문자열 조합

모든 명령을 처리한 후: `''.join(left) + ''.join(reversed(right))`
right 스택은 reversed해야 원래 순서가 된다.

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(N + M) — 초기 문자열 길이 + 명령 수 |
| 공간 | O(N + M) — 삽입된 문자까지 포함 |
