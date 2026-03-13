# Common Core Portfolio Module

> 모든 제출본의 첫 장에 붙는 공통 기반 모듈입니다.

| 항목 | 내용 |
| --- | --- |
| 공통 코어 | 42서울, `cs-core`, `network-atda`, `database-systems` |
| 대표 42 사례 | [`ft_transcendence`](https://github.com/animasyn/ft_transcendence) |
| 공통 메시지 | 문제를 작은 단위로 분해하고, 검증 가능한 실행 경로와 문서를 함께 남기는 개발자 |

## 42서울 정규과정

42서울 정규과정은 제 개발의 출발점이자, 이후 모든 프로젝트에서 유지한 문제 해결 방식의 뿌리입니다. C/C++ 기반 시스템 프로그래밍, 네트워크, 디버깅, 팀 과제를 통해 런타임과 실패 원인을 추적하는 습관을 만들었습니다.

상세 사례는 `ft_transcendence` 하나만 사용합니다. 이 프로젝트에서는 Django 백엔드를 전담했고, 42 OAuth 기반 원격 인증, JWT, TOTP 기반 2FA, OpenAPI 문서화를 포함한 인증/인가 흐름을 담당한 경험으로 정리합니다.

```text
README: Standard user management, remote authentication, 2FA and JWT
OpenAPI: /api/v1/auth/42/login
OpenAPI: /api/v1/auth/42/callback
OpenAPI: /api/v1/auth/token/refresh
OpenAPI: /api/v1/auth/2fa/setup
OpenAPI: /api/v1/auth/2fa/verify
Code trace: pyotp / jwt / temp_2fa / is_totp_enabled
```

`minishell`, `irc`, `raytracing`는 팀과제 맥락의 보조 사례로만 다룹니다. 세 프로젝트 모두 개인 파트를 과장해 적지 않고, 시스템 기초, 협업, 그래픽스/네트워크 경험을 넓힌 팀 단위 결과물로 정리합니다.

## 공통 학습 축

| 축 | 근거 | 의미 |
| --- | --- | --- |
| CS 기초 | [cs-core](../../../cs-core/README.md) | 시스템 프로그래밍, 런타임, 언어/인터프리터, 디버깅 기초 |
| 네트워크 | [network-atda](../../../network-atda/README.md) | TCP/UDP, reliable transport, routing, diagnostics, game server capstone |
| 데이터 | [database-systems](../../../database-systems/README.md) | SQL, storage, index, clustered KV capstone까지 이어지는 데이터 계층 이해 |

## 공통 습관

- 구현만이 아니라 `README`, `docs`, `notion`, `blog`를 분리해 설명 가능한 결과물을 남깁니다.
- 가능한 한 `test`, `smoke`, `demo` 같은 재현 경로를 문서 앞단에 둡니다.
- 문제를 기능 목록보다 경계와 검증 기준으로 먼저 정리합니다.

## 마무리

이 모듈은 특정 프레임워크보다 개발 방식의 기반을 보여 줍니다. 42서울에서 만든 시스템 감각과 현재 워크스페이스의 CS/네트워크/데이터 학습을 공통 배경으로 삼고, 이후 가지 문서에서 프론트엔드, 백엔드, 게임서버, 회사별 제출본으로 분기합니다.
