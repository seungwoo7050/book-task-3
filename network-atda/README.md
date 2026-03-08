
# Networking Study Archive

이 저장소는 *Computer Networking: A Top-Down Approach* 학습 자료를 `legacy/`와 `study/`로 분리해 정리한 공개용 study archive입니다.

## 핵심 원칙

- `legacy/`는 읽기 전용 참조 트리다.
- `study/`는 공개 가능한 학습 구조다.
- `docs/`는 커리큘럼, 검증 기준, 마이그레이션 규칙을 저장한다.
- `notion/`은 저장소 공개 구조와 분리된 업로드용 작업 노트다.

## study 트랙

- [`study/Application-Protocols-and-Sockets/README.md`](study/Application-Protocols-and-Sockets/README.md)
- [`study/Reliable-Transport/README.md`](study/Reliable-Transport/README.md)
- [`study/Network-Diagnostics-and-Routing/README.md`](study/Network-Diagnostics-and-Routing/README.md)
- [`study/Packet-Analysis-Top-Down/README.md`](study/Packet-Analysis-Top-Down/README.md)
- [`study/Game-Server-Capstone/README.md`](study/Game-Server-Capstone/README.md)

## canonical 검증 예시

- 파일럿 과제: `make -C study/Application-Protocols-and-Sockets/web-server/problem test`
- transport 과제: `make -C study/Reliable-Transport/rdt-protocol/problem test`
- 패킷 랩 전체: `make -C study/Packet-Analysis-Top-Down test`
- capstone: `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`

## 현재 공개 상태

- 모든 project는 새 `study/` 경로 기준 canonical 검증을 통과했다.
- raw socket을 직접 여는 live 실행은 `run-solution` 또는 `run-client`로 수동 재현할 수 있다.
- 외부 네트워크에 의존하는 live 결과는 문서 참고용이며, 기본 완료 상태 판정은 deterministic `make test` 기준으로 관리한다.

세부 상태는 [`docs/verification-matrix.md`](docs/verification-matrix.md)에서 관리한다.
