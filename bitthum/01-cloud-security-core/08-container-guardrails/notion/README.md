# 08 Container Guardrails — Notion 문서 안내

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트 08-container-guardrails의 전체 개발 과정과 학습 내용을
Notion으로 옮길 수 있는 형태로 정리한 문서 세트입니다.

## 문서 목록과 읽기 순서

| 순서 | 문서 | 목적 | 추천 독자 |
|------|------|------|-----------|
| 1 | [essay.md](essay.md) | EKS 없이도 컨테이너 보안을 학습할 수 있다는 발상과, manifest 검사의 실용성을 서사적으로 풀어낸 에세이 | 컨테이너 보안이 처음인 사람, K8s manifest 분석에 관심 있는 사람 |
| 2 | [dev-timeline.md](dev-timeline.md) | YAML 파싱부터 이미지 메타데이터 검사까지 전체 개발 과정의 타임라인 | 프로젝트를 재현하려는 사람 |

## 언제 어떤 문서를 읽을까

- **"EKS 없이 컨테이너 보안을 어떻게 학습하는지 알고 싶다"** → `essay.md`
- **"K8s manifest에서 잡을 수 있는 위험 설정이 뭔지 알고 싶다"** → `essay.md`의 규칙 섹션
- **"직접 guardrail scanner를 만들어 보고 싶다"** → `dev-timeline.md`
- **"insecure/secure manifest의 차이를 빠르게 비교하고 싶다"** → `dev-timeline.md`의 fixture 섹션
