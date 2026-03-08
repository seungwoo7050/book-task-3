# Notion Readiness Audit

`notion/`은 기본적으로 로컬 전용이며 `.gitignore` 대상이다. 다만 품질 기준은 공개 문서보다 낮아도 된다는 뜻이 아니다. 이 문서는 각 프로젝트의 `notion/`이 "지금 바로 노션으로 옮겨도 되는가"와 "그대로 공개 공유해도 되는가"를 분리해서 기록한다.

## 판정 축

- `notion-ready`: 문장이 완전하고, 문제 정의와 판단 근거, 불확실성이 적혀 있어 로컬 노트로 바로 쓸 수 있다.
- `public-share-ready`: 외부 독자가 읽어도 오해가 적고, 구현 또는 검증 근거가 충분해 공개 공유해도 된다.

## 현재 판정

| 프로젝트 | notion-ready | public-share-ready | 비고 |
| --- | --- | --- | --- |
| `frontend-foundations/01-semantic-layouts-and-a11y` | yes | yes | 구현, 테스트, landmark/keyboard 검증 근거가 있다 |
| `frontend-foundations/02-dom-state-and-events` | yes | yes | URL state, persistence, delegated interaction에 대한 구현과 테스트 근거가 있다 |
| `frontend-foundations/03-networked-ui-patterns` | yes | yes | abort, retry, query navigation에 대한 구현과 테스트 근거가 있다 |
| `react-internals/01-vdom-foundations` | yes | yes | 구현과 검증이 있고 노트가 실제 코드/문서와 연결된다 |
| `react-internals/02-render-pipeline` | yes | yes | diff/patch, scheduler 테스트와 구현 근거가 연결된다 |
| `react-internals/03-hooks-and-events` | yes | yes | hook, effect, delegated event 테스트와 구현 근거가 연결된다 |
| `react-internals/04-runtime-demo-app` | yes | yes | shared runtime demo, metrics, limitation docs와 테스트 근거가 있다 |
| `frontend-portfolio/01-ops-triage-console` | yes | yes | 구현, 테스트, 발표 문서와 연결된 실사용 근거가 있다 |
| `frontend-portfolio/02-client-onboarding-portal` | yes | yes | sign-in, draft restore, route guard, submit retry에 대한 구현과 검증 근거가 있다 |

## 해석 원칙

- `public-share-ready: no`는 품질 부족만 뜻하지 않는다. 구현/검증 증거가 없는 설계 단계 노트도 여기에 포함된다.
- `planned` 프로젝트의 `notion/`은 설계와 위험 관리 문서로서는 충분할 수 있다. 다만 공개 공유 시에는 "구현 전 설계 노트"라는 맥락을 반드시 붙여야 한다.
- `verified` 프로젝트라도 로컬 절대경로, 확인 불가능한 메타데이터, 의미 없는 링크 모음이 남아 있으면 `public-share-ready`를 줄 수 없다.

## 다음 갱신 조건

- 새 프로젝트가 `verified`로 올라가면 해당 `notion/`의 공개 공유 가능 여부를 다시 판정한다.
- `planned`에서 `in-progress`로 넘어갈 때는 `02-debug-log.md`에 실제 실패 사례가 생기는지 확인한다.
- 발표 자료나 README가 바뀌어 참고 경로가 달라지면 `04-knowledge-index.md`의 링크와 이 문서의 판정을 같이 갱신한다.
