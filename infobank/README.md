# Infobank 과제 학습 레포

이 저장소는 인포뱅크 과제를 풀이집처럼 정리하는 대신, "어떻게 문제를 해석하고 작은 학습 단위를 쌓아 최종 제출물과 포트폴리오로 연결하는가"를 보여 주는 학습 레포다. 목표는 다른 학생이 이 레포를 읽으며 자기만의 공개 포트폴리오 레포를 더 나은 구조로 설계할 수 있게 돕는 것이다.

현재는 두 개의 활성 트랙을 다룬다.

- `mcp-recommendation-demo/`: 1번 과제, MCP 추천 최적화
- `chat-qa-ops/`: 2번 과제, 챗봇 상담 품질 관리

## 현재 구조

```text
infobank/
├── docs/
├── mcp-recommendation-demo/
└── chat-qa-ops/
```

이 레포는 아직 `legacy/` 또는 `study/` 재배치 구조를 사용하지 않는다. 현재 루트 트랙 구조를 사실 기준으로 설명하고, 나중에 레거시 자료가 들어오더라도 읽기 전용 참조로만 취급한다.

## 문서 원칙

- 핵심 안내 문서는 한글 우선으로 쓴다.
- `README.md`, `problem/`, `docs/`는 처음 읽는 사람이 길을 잃지 않도록 현재 상태, 읽는 순서, 검증 경로를 빠르게 알려 준다.
- `notion/`도 레포에 포함한다. 과정 기록, 실패 메모, 회고, 지식 인덱스, 재현 타임라인을 공개 백업 문서로 함께 보관한다.
- `notion/`을 다시 정리할 때는 기존 폴더를 지우지 않는다. `notion-archive/`로 이름을 바꿔 남기고, 새 `notion/`을 만든다.
- 아직 구현하지 않았거나 검증하지 않은 내용은 솔직하게 `planned` 또는 미구현 상태로 적는다.

## 처음 읽는 순서

1. [`docs/README.md`](./docs/README.md)
2. [`docs/project-selection-rationale.md`](./docs/project-selection-rationale.md)
3. [`docs/curriculum-map.md`](./docs/curriculum-map.md)
4. [`chat-qa-ops/README.md`](./chat-qa-ops/README.md)
5. [`mcp-recommendation-demo/README.md`](./mcp-recommendation-demo/README.md)

바로 실행 가능한 결과물을 먼저 보고 싶다면 다음 순서를 권한다.

1. [`chat-qa-ops/08-capstone-submission/README.md`](./chat-qa-ops/08-capstone-submission/README.md)
2. [`chat-qa-ops/08-capstone-submission/v3-self-hosted-oss/README.md`](./chat-qa-ops/08-capstone-submission/v3-self-hosted-oss/README.md)
3. [`mcp-recommendation-demo/08-capstone-submission/README.md`](./mcp-recommendation-demo/08-capstone-submission/README.md)
4. [`mcp-recommendation-demo/08-capstone-submission/v3-oss-hardening/README.md`](./mcp-recommendation-demo/08-capstone-submission/v3-oss-hardening/README.md)

## 학생용 빠른 시작

- 처음 30분은 루트 README, `docs/README.md`, 각 트랙 README만 읽어도 충분하다.
- 그다음에는 관심 있는 트랙의 `08-capstone-submission/README.md`와 상위 `notion/05-development-timeline.md`를 함께 본다.
- 마지막으로 같은 트랙의 `00~07` stage를 거꾸로 훑으며 "이 capstone이 어떤 작은 학습 단위에서 올라왔는가"를 확인한다.

## 내 포트폴리오로 옮길 때 최소 구조

- `README.md`: 문제 해석, 현재 상태, 실행 명령, 읽기 순서를 짧게 적는다.
- `problem/README.md`: 제공 문제와 고정 범위를 분리해 둔다.
- `docs/README.md`: 오래 남길 개념, proof artifact, 검증 기준을 정리한다.
- `notion/05-development-timeline.md`: 읽기 순서, 실행 순서, 증거 대조 순서를 남긴다.
- 기존 노트를 다시 쓰고 싶다면 지우지 말고 `notion-archive/`로 옮긴다.

## 학생에게 이 레포가 주는 도움

- stage 단위 학습과 capstone 버전 스냅샷을 함께 보여 줘서 "작은 프로젝트를 어떻게 최종 제출물로 묶는가"를 따라갈 수 있다.
- README와 `docs/`만 읽어도 현재 구현 범위와 검증 경로를 파악할 수 있다.
- `notion/`과 `notion-archive/`를 함께 보면 생각이 어떻게 바뀌었는지, 어떤 문서를 새 기준으로 다시 썼는지까지 추적할 수 있다.
- 특히 `05-development-timeline.md`를 따라가면 "지금 이 레포를 읽는 순서"와 "내 레포에 같은 구조를 옮기는 순서"를 동시에 잡을 수 있다.
