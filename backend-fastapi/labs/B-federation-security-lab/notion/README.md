# B-federation-security-lab 학습 노트

이 폴더는 현재 공개용 학습 노트입니다. 외부 로그인과 2FA 흐름을 이 노트만으로 따라갈 수 있게 요약했습니다.

## 먼저 볼 문서

- 바로 손을 움직여 재현하고 싶다면 [05-development-timeline.md](05-development-timeline.md)부터 읽습니다.
- 왜 이런 구조로 만들었는지부터 이해하고 싶다면 `00`, `01`부터 읽습니다.

## 추천 읽기 순서

1. [00-problem-framing.md](00-problem-framing.md)
2. [01-approach-log.md](01-approach-log.md)
3. [02-debug-log.md](02-debug-log.md)
4. [03-retrospective.md](03-retrospective.md)
5. [04-knowledge-index.md](04-knowledge-index.md)
6. [05-development-timeline.md](05-development-timeline.md)

## 어떻게 쓰면 좋은가

- 실행 재현이 최우선이면 `05`를 먼저 보고, 외부 로그인과 2FA가 왜 그렇게 흘러가는지는 `01`, `02`에서 보완합니다.
- 외부 로그인과 2FA의 설계 경계를 보고 싶으면 `00`, `01`부터 읽습니다.
- 실제로 헷갈리기 쉬운 인프라/쿠키 문제는 `02`에서 빠르게 확인할 수 있습니다.
- 포트폴리오 확장 아이디어는 `03`, `04`에 정리했습니다.
