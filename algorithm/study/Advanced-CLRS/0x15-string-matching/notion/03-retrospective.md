# 회고

> 프로젝트: 고급 문자열 매칭
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

- KMP: 결정론적, 최악 $O(n+m)$ 보장. prefix function이 핵심 전처리.
- Rabin-Karp: 기대 $O(n+m)$, 해시 충돌 시 최악 $O(nm)$. 다중 패턴 검색에 유리.
- 두 알고리즘의 트레이드오프: KMP는 단일 패턴에 안정적, Rabin-Karp는 다중 패턴/2D 매칭에 확장성.

## 실무 연결

`grep -F`는 Aho-Corasick (KMP 확장), `grep -E`는 NFA/DFA. Rabin-Karp는 plagiarism detection에 활용.

## 이번 프로젝트가 남긴 기준

- `고급 문자열 매칭`를 통해 `고급 문자열 매칭의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- CLRS Ch 32의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../0x14-network-flow/README.md`](../../0x14-network-flow/README.md) (네트워크 플로우)
- 다음 프로젝트: [`../../0x16-computational-geometry/README.md`](../../0x16-computational-geometry/README.md) (계산 기하 실습)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`string-matching-concept.md`](../docs/concepts/string-matching-concept.md)
