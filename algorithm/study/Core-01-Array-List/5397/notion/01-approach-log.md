# 접근 로그

> 프로젝트: 키로거
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 1406에서 가져온 패턴

Two-Stack 모델을 그대로 적용했다.
- `<` → left에서 pop → right에 push
- `>` → right에서 pop → left에 push
- `-` → left에서 pop (버림)
- 문자 → left에 push

차이점은 명령이 별도 줄이 아니라 한 줄의 문자열 안에 섞여 있다는 것이다.
하지만 한 글자씩 순회하면서 동일한 분기를 타면 된다.

## 출력 최적화

테스트 케이스가 최대 1,000개이고 총 키 입력이 $5 \times 10^6$이다.
각 테스트 케이스마다 `print()`를 쓰면 오버헤드가 쌓일 수 있다.
`sys.stdout.write()`로 개행까지 직접 제어하는 게 더 안전하다.

실제 코드에서도 `sys.stdout.write(''.join(left) + ''.join(reversed(right)) + '\n')`을 사용했다.

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(총 키 입력 길이) |
| 공간 | O(총 키 입력 길이) |

## 이 접근에서 꼭 기억할 선택

- `키로거`에서 중심이 된 판단은 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`keylogger-concept.md`](../docs/concepts/keylogger-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
