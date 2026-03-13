# 09 Exception and Evidence Manager 읽기 지도

finding 이후의 거버넌스를 exception, evidence, audit trail로 분리해 모델링하는 작은 상태 관리기다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 왜 예외를 mute 플래그가 아니라 record 집합으로 봐야 하는가?
- approval과 expiry가 suppression 판정에 어떻게 연결되는가?
- evidence append와 append-only audit trail이 왜 함께 필요했는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. 예외와 증적과 감사를 record로 분리했다: 예외 관리를 단순 플래그가 아니라 추적 가능한 데이터 모델로 바꾼다.
3. Phase 2. approval과 expiry를 suppression 판정에 연결했다: 예외가 언제 finding을 실제로 억제하는지 코드로 정의한다.
4. Phase 3. evidence append와 append-only audit trail을 잠갔다: 예외 흐름의 근거와 변경 이력이 함께 남는지 검증한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- 예외를 mute가 아닌 record 집합으로 다루는 전환을 먼저 보여 준다.
- approval과 expiry를 suppression 판정과 연결하는 부분을 중간 축으로 둔다.
- evidence append와 append-only audit trail을 마지막 증거로 사용한다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): exception, evidence, audit를 따로 모델링하기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/governance-flow.md`
- `python/src/exception_evidence_manager/manager.py`
- `python/src/exception_evidence_manager/cli.py`
- `python/tests/test_manager.py`
