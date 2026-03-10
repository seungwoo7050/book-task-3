# Debug Log — "authorization lab"이라는 이름의 무게

## 마주한 문제

이 랩에서도 런타임 버그보다 **구현 깊이와 문서 설명 사이의 간극**이 핵심 문제였다.

organization 생성, invite, role change가 동작하더라도, Spring method security(`@PreAuthorize`, `@Secured`)가 없으면 "authorization lab"이라는 이름이 과장되어 보일 수 있다. RBAC API surface만 있으면 authorization 구현이 충분히 깊어 보일 것이라는 가정은 잘못이었다.

## 근본 원인

authorization 문제에서 진짜 중요한 건 **API surface가 아니라 enforcement 위치**다. "이 엔드포인트가 있다"는 것과 "이 엔드포인트에 권한 체크가 걸려 있다"는 것은 다른 문제다. 현재 scaffold는 service logic에서 `if (!organization.members().containsKey(email))`로 체크하지만, Spring Security의 declarative policy(`@PreAuthorize("hasRole('OWNER')")`)까지는 가지 않았다.

## 어떻게 해결했는가

docs에서 current implementation과 next improvements를 명확히 분리했다. 현재는 **service logic 중심 scaffold**라는 점을 전면에 내세우고, method annotation 기반 enforcement는 "다음 단계"로 분류했다.

```bash
make test    # AuthorizationApiTest — invite → accept → role change 흐름 통과
make smoke   # 앱 기동 확인
```

## 남아 있는 기술 부채

- **forbidden-path 테스트 부족**: 현재 테스트는 "성공 경로"만 검증한다. "STAFF가 role change를 시도하면 403" 같은 거부 경로 테스트가 필요하다.
- **method annotation 기반 enforcement**: `@PreAuthorize`로 authorization rule을 옮기면, service logic에서 권한 체크 코드가 사라지고 선언적으로 관리할 수 있다.

