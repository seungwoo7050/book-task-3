# 회고

> 프로젝트: 팰린드롬인지 확인하기
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 이 문제가 남긴 것

회문 판별 자체는 5분이면 끝나는 문제였다.
하지만 이 프로젝트를 진행하면서 실제로 시간이 간 부분은 **코드가 아니라 구조**였다.

### 프로젝트 구조를 처음 잡는 연습

이 문제가 Core-00-Basics의 첫 번째 프로젝트였기 때문에,
`problem/`, `python/`, `docs/`, `notion/`으로 나누는 디렉터리 구조를 여기서 확립했다.

나중에 수십 개의 문제를 풀면서 이 구조가 일관되게 유지된다.
결국 첫 번째 문제에서 구조를 제대로 잡은 덕분에, 이후 문제에서는 구조에 대해 고민할 필요가 없었다.

### sys.stdin.readline의 습관화

`input()` 대신 `sys.stdin.readline`을 쓰는 습관을 여기서 시작했다.
이 문제에서는 성능 차이가 없지만, 나중에 대량 입력 문제에서 이 습관이 살아남았다.

### Makefile 기반 검증 흐름

`make -C problem test`라는 한 줄로 검증하는 패턴을 여기서 처음 쓰기 시작했다.
테스트 스크립트(`script/test.sh`)가 fixture를 자동으로 순회하는 구조도 이때 만들었다.

## 다음에 적용할 것

- 투 포인터 방식은 다음에 문자열 길이가 큰 문제에서 시도해 볼 것
- edge case 문서화를 별도 파일로 분리하는 패턴은 계속 유지할 것

## 이번 프로젝트가 남긴 기준

- `팰린드롬인지 확인하기`를 통해 `작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 다음 프로젝트: [`../../11053/README.md`](../../11053/README.md) (가장 긴 증가하는 부분 수열)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`palindrome-concept.md`](../docs/concepts/palindrome-concept.md)
