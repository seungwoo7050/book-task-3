# Repository Inventory

## 현재 루트 구조

```text
network-atda/
  README.md
  docs/
  study/
```

## 디렉터리 역할

- `README.md`: 저장소 전체 목적, 학습 순서, 프로젝트 카탈로그, 검증 빠른 시작
- `docs/`: 저장소 수준 문서와 README 계약
- `study/`: 실제 학습 단계와 프로젝트

## `study/` 안의 현재 단계

- `01-Application-Protocols-and-Sockets`
- `02-Reliable-Transport`
- `03-Packet-Analysis-Top-Down`
- `04-Network-Diagnostics-and-Routing`
- `05-Game-Server-Capstone`

## 현재 프로젝트 개수

- 단계: `5`
- 프로젝트: `17`
- 구현 과제(`python/`, `cpp/`): `10`
- 패킷 분석 과제(`analysis/`): `7`
- `notion/`을 갖는 프로젝트: `10`
- `notion-archive/`를 갖는 프로젝트: `10`

## 프로젝트 공통 구조

- `README.md`: 프로젝트 인덱스와 학습 가이드
- `problem/`: 문제 설명, 제공 코드/데이터/스크립트, canonical 검증 진입점
- `python/` 또는 `cpp/` 또는 `analysis/`: 공개 구현 또는 공개 답안
- `docs/`: 반복해서 참고할 개념 문서
- `notion/`: 공개 백업용 학습 노트
- `notion-archive/`: 이전 형식의 노트를 보존할 때만 존재하는 선택 디렉터리

## 저장소 해석 원칙

- 문서는 현재 존재하는 소스와 디렉터리만 기준으로 씁니다.
- `problem/`과 구현/답안 디렉터리를 분리해 제공 자료와 사용자 작업을 섞지 않습니다.
- 최상위는 학습 단계 순서로 정렬하고, 프로젝트 README는 같은 공개 계약을 반복합니다.
