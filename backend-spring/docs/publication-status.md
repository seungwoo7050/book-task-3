# backend-spring 공개 포지셔닝

이 레포는 공개 가능한 학습 레포이지만, 무엇을 증명했고 무엇을 아직 증명하지 않았는지 정확하게 설명해야 합니다.

## 안전한 설명 방식

다음 같은 표현을 권장합니다.

- Java/Spring 백엔드 학습 트랙
- 독립 랩과 커머스 캡스톤으로 구성된 학습 결과물 레포
- verified scaffold 랩과 더 강한 portfolio-grade capstone

다음 같은 표현은 피합니다.

- production-ready commerce platform
- 완전한 Spring Security reference implementation
- end-to-end cloud-verified system

## 지금 강한 점

- 모든 랩과 캡스톤이 독립 실행 가능하게 정리되어 있습니다.
- README, docs, notion이 각각 다른 역할을 맡고 있어 읽는 순서가 분리되어 있습니다.
- lint, test, smoke, Compose health 확인 기록이 남아 있습니다.
- Spring Security, JPA, PostgreSQL, Redis, Kafka, Docker 같은 채용 공고 키워드를 실제 문제 맥락 안에서 설명할 수 있습니다.

## 아직 발표 시 주의할 점

- 몇몇 랩은 실제 통합보다 contract modeling과 사고방식을 보여주는 단계입니다.
- Google OAuth, Redis-heavy caching, Kafka 장기 운영 특성, AWS 배포는 부분적으로만 검증되었습니다.
- `commerce-backend-v2`도 강한 학습 결과물이지만, production commerce platform을 주장하는 수준은 아닙니다.

## 추천 저장소 설명

`Spring Boot 백엔드에서 반복적으로 만나는 문제를 독립 랩으로 학습하고, 마지막에 커머스 캡스톤으로 다시 조합한 학습용 레포`
