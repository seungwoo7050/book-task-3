# Repository Inventory

## 현재 루트 구조

```text
network-atda/
  README.md
  docs/
  study/
```

## 디렉터리 역할

- `README.md`: 저장소 전체 목적, 학습 순서, 검증 원칙, 포트폴리오 가이드
- `docs/`: 저장소 수준 문서
- `study/`: 실제 학습 트랙과 프로젝트

## `study/` 안의 현재 트랙

- `Application-Protocols-and-Sockets`
- `Reliable-Transport`
- `Packet-Analysis-Top-Down`
- `Network-Diagnostics-and-Routing`
- `Game-Server-Capstone`

## 현재 프로젝트 개수

- 트랙: `5`
- 프로젝트: `17`
- 구현 과제(`python/`, `cpp/`): `10`
- 패킷 분석 과제(`analysis/`): `7`
- 새 형식 `notion/`을 갖는 프로젝트: `10`
- 과거 형식 백업 `notion-archive/`를 갖는 프로젝트: `10` 예정

## 프로젝트 공통 구조

- `README.md`: 프로젝트 인덱스와 학습 가이드
- `problem/`: 문제 설명, 제공 코드/데이터/스크립트, canonical 검증 진입점
- `python/` 또는 `cpp/` 또는 `analysis/`: 공개 구현 또는 공개 답안
- `docs/`: 반복해서 참고할 개념 문서
- `notion/`: 공개 백업용 학습 노트
- `notion-archive/`: 이전 형식의 노트를 보존할 때만 존재하는 선택 디렉터리

## 저장소 해석 원칙

- 문서는 현재 존재하는 소스와 디렉터리만 기준으로 씁니다.
- `problem/`과 구현/답안 디렉터리를 분리해, 제공 자료와 사용자 작업을 섞지 않습니다.
- `README.md`는 빠르게 길을 찾게 하는 인덱스 역할을 맡고, 자세한 과정 기록은 `notion/`으로 넘깁니다.
