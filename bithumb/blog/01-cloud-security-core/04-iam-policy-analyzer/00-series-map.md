# 04 IAM Policy Analyzer 읽기 지도

allow/deny 평가를 끝내지 않고, least privilege 관점의 triage 가능한 finding으로 바꾸는 단계다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 왜 allow/deny 결과 위에 finding 구조를 한 겹 더 얹어야 했는가?
- broad admin을 왜 두 control로 분리했는가?
- escalation action과 safe policy 0건이 rule 품질을 어떻게 결정했는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. finding 스키마를 먼저 고정했다: 정책 위험을 remediation과 이어질 수 있는 구조화된 finding으로 표현한다.
3. Phase 2. broad admin을 두 control로 분해했다: `Action=*`와 `Resource=*`가 남기는 운영 질문을 분리한다.
4. Phase 3. escalation action과 false positive 경계를 함께 고정했다: 정책이 넓지 않더라도 privilege escalation 위험이 있는 경우를 별도 control로 잡고, safe fixture 0건도 확인한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- decision engine에서 risk analyzer로 질문이 바뀌는 지점을 도입에서 선명하게 잡는다.
- broad admin을 두 control로 나누는 장면을 첫 번째 핵심 분기점으로 둔다.
- escalation action과 safe policy 0건 테스트를 후반부에 묶어 false positive 기준을 설명한다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): allow/deny를 risk finding으로 바꾸기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/least-privilege-findings.md`
- `python/src/iam_policy_analyzer/analyzer.py`
- `python/src/iam_policy_analyzer/cli.py`
- `python/tests/test_analyzer.py`
