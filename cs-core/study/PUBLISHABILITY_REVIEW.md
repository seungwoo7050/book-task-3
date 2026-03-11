# Study 공개 범위 검토

## 이 문서가 다루는 것

이 문서는 `study/` 트리에서 무엇을 공개 저장소에 남기고, 무엇을 로컬에서만 복원해야 하는지 정리합니다.
2026-03-10 문서 정비 기준으로 다시 정리한 정책입니다.

## 저장소 전체 원칙

- 공개 가능:
  - `c/`, `cpp/`, `y86/`, `docs/`, `tests/`, `notion/`
  - 필요할 때 유지하는 로컬 백업 성격의 `notion-archive/` 또는 유사 폴더
  - 스터디용으로 직접 작성한 `problem/` 경계 문서와 보조 스크립트
- 로컬 전용:
  - 공식 핸드아웃 원본
  - 공식 바이너리와 복원 툴체인
  - 쿠키 파일, course-instance 전용 정답, 타깃별 민감 자산

`notion/`은 더 이상 "git에 올리지 않는 임시 노트"가 아닙니다.
Notion 업로드용 문서이면서 저장소 안에 백업으로 유지하는 추적 대상입니다.

## 프로젝트별 판단

### `Foundations-CSAPP/datalab`

- 공개 가능: 자체 작성한 문제 경계, C/C++ 구현, `docs/`, `notion/`
- 로컬 전용: `problem/official/`에 복원되는 공식 self-study handout과 `dlc`

### `Foundations-CSAPP/bomblab`

- 공개 가능: 문제 계약 설명, companion 구현, 워크플로 문서, 공개 self-study bomb용 검증 파일
- 로컬 전용: 복원한 공식 bomb 바이너리와 외부 course-instance 전용 답안

### `Foundations-CSAPP/attacklab`

- 공개 가능: 문제 계약 설명, companion verifier, 공개 self-study target용 샘플, 방어 모델 설명
- 로컬 전용: 복원한 `ctarget`, `rtarget`, `hex2raw`, 타깃별 쿠키

### `Foundations-CSAPP/archlab`

- 공개 가능: 문제 경계 문서, `y86/` 학습 산출물, companion 구현, 문서와 노트
- 로컬 전용: 복원한 simulator/HCL toolchain

### `Foundations-CSAPP/perflab`

- 공개 가능: 문제 경계, sample trace, C/C++ 구현, 문서와 노트
- 로컬 전용: 없음

### `Systems-Programming/shlab`

- 공개 가능: self-written 문제 계약, 자체 테스트, C/C++ 구현, 문서와 노트
- 로컬 전용: 공식 starter shell과 공식 traces가 필요한 경우 직접 복원한 사본

### `Systems-Programming/malloclab`

- 공개 가능: allocator contract, `memlib`, traces, driver, C/C++ 구현, 문서와 노트
- 로컬 전용: 없음

### `Systems-Programming/proxylab`

- 공개 가능: proxy starter boundary, socket helpers, tests, origin harness, C/C++ 구현, 문서와 노트
- 로컬 전용: 없음

### `Operating-Systems-Internals/scheduling-simulator`

- 공개 가능: self-authored fixture, Python 구현, `docs/`, `notion/`, canonical `problem/Makefile`
- 로컬 전용: 없음

### `Operating-Systems-Internals/virtual-memory-lab`

- 공개 가능: self-authored trace fixture, Python 구현, `docs/`, `notion/`, canonical `problem/Makefile`
- 로컬 전용: 없음

### `Operating-Systems-Internals/filesystem-mini-lab`

- 공개 가능: self-authored JSON image model, Python 구현, `docs/`, `notion/`, canonical `problem/Makefile`
- 로컬 전용: 없음

### `Operating-Systems-Internals/synchronization-contention-lab`

- 공개 가능: self-authored C 구현, shell test, `docs/`, `notion/`, canonical `problem/Makefile`
- 로컬 전용: 없음

### `Programming-Languages-Foundations/parser-interpreter`

- 공개 가능: self-authored toy language source, `examples/`, Python 구현, 테스트, `docs/`, `notion/`, `notion-archive/`
- 로컬 전용: 없음

### `Programming-Languages-Foundations/static-type-checking`

- 공개 가능: self-authored type rule fixture, Python checker 구현, 테스트, `docs/`, `notion/`, `notion-archive/`
- 로컬 전용: 없음

### `Programming-Languages-Foundations/bytecode-ir`

- 공개 가능: self-authored bytecode lowering fixture, Python compiler/VM 구현, disassembly golden test, `docs/`, `notion/`, `notion-archive/`
- 로컬 전용: 없음

## 공개 저장소에서 지킬 선

- README와 `docs/`는 학습 가이드 역할을 해야 하며, 외부 제공 자산의 무단 재배포 수단이 되어서는 안 됩니다.
- `bomblab`, `attacklab`은 풀이 사고법을 설명하되, 외부 비공개 타깃에 바로 적용 가능한 정보는 공개하지 않습니다.
- 공식 자산 복원이 필요한 프로젝트는 `problem/README.md`에 복원 절차만 기록하고, 자산 자체는 커밋하지 않습니다.

## 포트폴리오로 확장하는 힌트

- 개인 저장소에서도 이 정책을 그대로 재사용하면 공개 가능 여부 판단이 훨씬 쉬워집니다.
- 특히 외부 과제 기반 프로젝트는 "문제 계약 요약 + 복원 절차 + 본인 구현" 구조가 가장 안전합니다.
