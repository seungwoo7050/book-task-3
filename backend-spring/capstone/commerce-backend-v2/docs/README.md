# commerce-backend-v2 아키텍처 문서 지도

이 폴더는 대표 capstone의 설계 설명과 검증 메모를 모아 둔 곳이다.

## 먼저 읽을 문서

- [architecture-overview.md](architecture-overview.md): 패키지 경계와 주요 데이터 흐름을 한 번에 본다
- [domain-model-and-state-transitions.md](domain-model-and-state-transitions.md): order, payment, notification 상태 전이를 본다
- [interview-talking-points.md](interview-talking-points.md): 면접에서 이 프로젝트를 어떤 순서로 설명할지 정리한다
- [deployment-note-ecs-rds-elasticache.md](deployment-note-ecs-rds-elasticache.md): AWS 지향 배포 메모를 확인한다
- [verification.md](verification.md): 실제 재검증 범위와 남은 한계를 확인한다

## 이 문서들이 답하는 질문

- 왜 microservice가 아니라 modular monolith를 선택했는가
- Redis와 Kafka를 어디에만 제한적으로 사용했는가
- baseline 대비 무엇이 더 깊어졌는가
- 현재 검증이 무엇을 증명하고 무엇을 아직 증명하지 못하는가
