# 05-auth-and-authorization series map

`05-auth-and-authorization`는 request pipeline 위에 보안 규칙이 처음 올라가는 단계다. 그래서 이 시리즈는 "JWT를 어떻게 만들었는가"보다 "공개 경로, 인증 필요 경로, 권한 필요 경로를 어떤 체인으로 나눴는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 Express에서 middleware chain을 먼저 만들고, NestJS에서 guard chain으로 같은 규칙을 재구성하는 순서로 복원한다.
- 근거는 `auth.middleware.ts`, `role.middleware.ts`, `auth.service.ts`, `roles.guard.ts`, 두 레인의 e2e 출력이다.

## 대표 검증

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   JWT 발급, 인증/인가 체인, e2e 경계 검증이 어떤 순서로 붙었는지 따라간다.
