# 08 Container Guardrails 읽기 지도

실제 클러스터 없이도 manifest와 image metadata만으로 설명 가능한 컨테이너 보안 규칙을 만드는 scanner다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 클러스터 없이도 어떤 manifest 규칙은 충분히 설명 가능한가?
- 왜 image metadata를 같은 scanner 문맥에 붙였는가?
- secure fixture 0건이 guardrail의 품질을 어떻게 보장하는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. manifest에서 설명 가능한 위험 설정을 먼저 골랐다: 클러스터 없이도 static file만 읽고 설명할 수 있는 규칙을 고른다.
3. Phase 2. securityContext를 broad privilege 신호로 묶었다: `latest`, `privileged`, root 실행, `ALL` capability 같은 위험 신호를 container-level finding으로 만든다.
4. Phase 3. image metadata와 secure fixture 0건으로 경계를 닫았다: manifest 외부의 이미지 정보도 같은 scanner에서 다루고, 안전한 입력은 조용히 지나가게 한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- manifest scanner가 pod template까지 내려가는 흐름을 먼저 보여 준다.
- image metadata scanner를 붙여 source가 달라도 finding 언어는 같다는 점을 강조한다.
- secure fixture 0건으로 guardrail의 경계를 마감한다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): manifest와 image metadata로 guardrail 세우기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/container-guardrails.md`
- `python/src/container_guardrails/scanner.py`
- `python/src/container_guardrails/cli.py`
- `python/tests/test_scanner.py`
