# notion/ — GitOps 배포

이 디렉토리는 프로젝트 16 (GitOps Deploy)의 학습 과정을 블로그형 에세이로 기록합니다.

## 파일 목록

| 파일 | 내용 |
|------|------|
| [00-problem-framing.md](./00-problem-framing.md) | 왜 GitOps로 배포하는가 |
| [01-approach-log.md](./01-approach-log.md) | Dockerfile, Helm, ArgoCD 구현 과정 |
| [02-debug-log.md](./02-debug-log.md) | 컨테이너 빌드, Helm 템플릿, ArgoCD 설정에서 만난 문제들 |
| [03-retrospective.md](./03-retrospective.md) | 인프라를 코드로 다루며 배운 것 |
| [04-knowledge-index.md](./04-knowledge-index.md) | 다룬 개념 정리 |
| [05-development-timeline.md](./05-development-timeline.md) | CLI 명령어와 인프라 구성 타임라인 |

## 연관 프로젝트

- [06-go-api-standard](../../01-backend-core/06-go-api-standard/) — Dockerfile의 대상 애플리케이션
- [14-cockroach-tx](../14-cockroach-tx/) — DB 연결 설정이 Helm values에 반영
- [17-game-store-capstone](../../04-capstone/17-game-store-capstone/) — 캡스톤에서 이 배포 파이프라인 활용
