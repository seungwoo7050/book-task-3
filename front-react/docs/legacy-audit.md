# Legacy Audit

`legacy/`는 참고 가치가 높지만, 그대로 활성 학습 저장소로 쓰기에는 몇 가지 구조적 문제가 있다.

## 확인된 사실

- 현재 루트에는 원래 `study/`, `docs/`, `.gitignore`가 없었다.
- 레거시 온보딩 문서는 더 이상 존재하지 않는 `react-dev/` 루트를 가정했다.
- 각 레거시 프로젝트는 `problem/`, `solve/`, `docs/`, `devlog/`를 갖고 있었지만, 활성 학습 경로와 참조 경로가 섞여 있었다.
- `legacy/**/node_modules`는 현재 환경에서 바로 신뢰할 수 없다.
- 레거시 문서의 "검증됨" 표시는 과거 시점의 실행 기록이며, 새 워크스페이스에서 다시 검증해야 한다.

## 레거시 프로젝트별 재매핑

| 레거시 프로젝트 | 강점 | 한계 | 새 매핑 |
| --- | --- | --- | --- |
| `virtual-dom` | 문제, 스켈레톤, 구현, 테스트, 개념 문서가 균형 있게 갖춰져 있다 | 학습 기록이 `devlog`와 `analysis`에 섞여 있고 루트 경로 설명이 오래됐다 | `react-internals/01-vdom-foundations` |
| `reconciliation` | diff/patch 단위가 명확하고 테스트도 분리돼 있다 | 세부 학습 단위로는 좋지만 전체 코어 경로에서는 더 긴 render pipeline 맥락이 필요하다 | `react-internals/02-render-pipeline` |
| `fiber-architecture` | render/commit 경계를 분명히 보여 준다 | 단독 단계로 두면 주니어 경로가 길어진다 | `react-internals/02-render-pipeline` |
| `hooks-from-scratch` | hook 슬롯 모델과 effect lifecycle 설명이 좋다 | public docs와 private logs의 경계가 모호하다 | `react-internals/03-hooks-and-events` |
| `mini-react` | 이벤트 시스템과 런타임 통합 구현이 강하다 | 이벤트 위임과 통합 런타임이 한 단계에 겹쳐 있어 학습 단위가 크다 | `react-internals/03-hooks-and-events` |
| `platform-capstone` | 데모 앱과 기능 모듈, 계측 관점이 잘 정리돼 있다 | self-contained `framework.ts`가 누적형 학습 흐름을 끊는다 | `react-internals/04-runtime-demo-app` |

## 재설계 결론

- `legacy/`는 계속 유지한다.
- 활성 학습은 `study/`로 분리한다.
- 공통 규칙은 `docs/`로 분리한다.
- 레거시 React internals 6단계는 주니어 끝자락 기준으로 4개 핵심 단계 + 세부 부록으로 압축한다.
- 레거시에 없는 웹 기초와 고객-facing 제품형 포트폴리오는 `study/`에서 새로 설계한다.
