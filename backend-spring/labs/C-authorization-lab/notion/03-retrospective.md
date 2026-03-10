# Retrospective — 인가 랩을 마치고 돌아보며

## 나아진 점

authorization을 auth와 분리해서 다룬 순서는 결과적으로 맞았다. "로그인은 되는데 이 API를 쓸 수 없다"라는 시나리오를 독립적으로 사고할 수 있게 됐다.

invite lifecycle을 넣은 덕분에 단순한 role toggle보다 훨씬 현실적인 membership model이 보였다. 실제 서비스에서 "즉시 멤버 추가"보다 "초대 → 수락" 패턴을 쓰는 이유가 invite 상태를 통해 감사 추적과 취소가 가능하기 때문이라는 걸 코드로 체감했다.

ownership과 membership을 나눠 생각하는 연습도 생겼다. "OWNER도 결국 role의 하나"라는 점, 그리고 "조직 생성자만 할 수 있는 것"과 "MANAGER가 할 수 있는 것"이 다르다는 점을 구조적으로 이해하게 됐다.

## 여전히 약한 부분

**인메모리 state**는 persistence 문제를 완전히 가린다. 서버가 재시작되면 모든 조직, 초대장, 멤버십이 사라진다. 실제 서비스에서는 이 데이터가 PostgreSQL에 저장되어야 하고, 트랜잭션 경계도 고려해야 한다.

**Spring method security로 넘어가는 다리가 아직 약하다.** 현재는 service logic에서 `if`문으로 권한을 체크하는데, `@PreAuthorize`로 전환할 때 "어디까지를 annotation으로 옮기고, 어디부터를 service logic에 남길 것인가"라는 설계 판단 기준이 아직 없다.

**거부 경로(denial-path) 테스트가 부족하다.** 성공 경로만 테스트하면, "권한이 없을 때 정말 거부되는지"를 증명할 수 없다.

## 다시 살펴볼 것들

**단기**: membership persistence를 PostgreSQL로 옮기기. JPA entity로 Organization, Membership, Invitation 테이블을 설계하고 Flyway 마이그레이션을 추가한다.

**중기**: `@PreAuthorize` 같은 method security로 재구성. "이 메서드는 OWNER만 호출 가능"을 annotation 한 줄로 표현할 수 있게 되면, service logic이 훨씬 깔끔해진다.

**장기**: capstone의 commerce 도메인에서 "상점 주인만 상품을 수정할 수 있다"는 실제 비즈니스 규칙에 이 랩의 authorization 패턴을 적용해 본다.

