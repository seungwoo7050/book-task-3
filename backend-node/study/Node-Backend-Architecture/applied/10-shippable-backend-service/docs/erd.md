# ERD

## 핵심 엔티티

```text
users
- id (uuid, pk)
- username (varchar(30), unique)
- password (varchar(100))
- role (varchar(10))
- createdAt (timestamptz)

books
- id (uuid, pk)
- title (varchar(200))
- author (varchar(100))
- publishedYear (int)
- genre (varchar(50))
- price (double precision)
- createdAt (timestamptz)
- updatedAt (timestamptz)
```

## 관계 해석

- 현재 schema에는 직접적인 foreign key가 없다.
- 의도는 “auth users”와 “catalog books”를 느슨하게 유지하는 것이다.
- 이벤트 시스템이 side effect 연결 지점 역할을 맡고 있으므로, 이 과제에서는 도메인 관계보다 운영 재현성과 API 명확성이 더 중요하다.
