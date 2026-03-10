# 회고

> 프로젝트: 키로거
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 이 문제가 남긴 것

1406을 풀고 와서 5397을 보면 즉시 "같은 구조"라는 걸 알아챈다.
하지만 1406을 풀지 않았다면, 이 문제를 처음부터 풀어야 했을 것이다.
**패턴을 축적하고, 새 문제에서 그 패턴을 인식하는 것**이 알고리즘 학습의 핵심이라는 걸 여기서 다시 확인했다.

### sys.stdout.write의 습관화

대량 출력 문제에서는 `print()` 대신 `sys.stdout.write()`를 쓰는 것이 Python에서의 관용적 최적화다.
이 습관은 이후 많은 문제에서 계속 적용된다.

## 다음에 적용할 것

- 새 문제를 만나면 "이전에 비슷한 구조를 본 적 있는가?"를 먼저 자문
- 출력이 많은 문제에서는 sys.stdout.write 기본 사용

## 이번 프로젝트가 남긴 기준

- `키로거`를 통해 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../10807/README.md`](../../10807/README.md) (개수 세기)
- 다음 프로젝트: [`../../1406/README.md`](../../1406/README.md) (에디터)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`keylogger-concept.md`](../docs/concepts/keylogger-concept.md)
