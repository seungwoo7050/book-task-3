# Attack Lab

## 이 프로젝트가 가르치는 것

`attacklab`은 스택 레이아웃, 제어 흐름 탈취, 코드 주입, ROP, 상대 주소 계산을 단계적으로 익히게 하는 프로젝트입니다.
동시에 공개 가능한 학습 기록과 민감한 exploit 정보의 경계를 어떻게 유지할지도 함께 배우게 합니다.

## 누구를 위한 문서인가

- 버퍼 오버플로와 ROP를 구조적으로 이해하고 싶은 학습자
- 공식 타깃 복원 절차와 companion verifier의 역할을 구분해서 보고 싶은 사람
- 보안 주제를 공개 저장소에서 안전하게 다루는 문서 구조가 필요한 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`docs/README.md`](docs/README.md)
3. [`c/README.md`](c/README.md)
4. [`cpp/README.md`](cpp/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
attacklab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

공식 self-study target 검증:

```bash
cd problem
make restore-official
make verify-official
```

C companion 검증:

```bash
cd c
make clean && make test
```

C++ companion 검증:

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- 공개 문서는 payload 사고법과 방어 기법 차이를 설명합니다.
- 비공개 course target에 바로 적용 가능한 raw exploit 정보는 늘리지 않습니다.
- `problem/official/` 아래 복원되는 타깃과 쿠키 파일은 로컬 전용 자산입니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 "어떤 제약이 공격 표면을 바꾸는가"를 설명하기 좋습니다.
- 개인 저장소에서는 phase별로 바이트 배열을 어떻게 해석했는지 도식으로 정리하면 전달력이 커집니다.
